import asyncio
import cProfile
import pstats
import io

from app.db.database import get_sessionmaker
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services.ticket_service import TicketService


async def test_crud():
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as db:

        service = TicketService(db)

        # ==========================================
        # 1. CREATE TICKET
        # ==========================================
        print("\n1. Creating ticket...")

        create_data = TicketCreate(
            title="cProfile Test",
            description="Testing service performance",
            priority="High",
        )

        created_ticket = await service.create_ticket(create_data)

        print("Created Ticket ID:", created_ticket.id)

        ticket_id = created_ticket.id


        # ==========================================
        # 2. GET ALL TICKETS
        # ==========================================
        print("\n2. Getting all tickets...")

        tickets = await service.get_all_ticket()

        print("Total tickets:", len(tickets))


        # ==========================================
        # 3. GET SINGLE TICKET
        # ==========================================
        print("\n3. Getting single ticket...")

        ticket = await service.get_ticket(ticket_id)

        print("Ticket ID:", ticket.id)


        print("\n4. Updating ticket...")

        update_data = TicketUpdate(
            title="Updated cProfile Test"
        )

        updated_ticket = await service.update_ticket(
            ticket_id,
            update_data
        )

        print("Updated Ticket ID:", updated_ticket.id)


        print("\n5. Deleting ticket...")

        await service.delete_ticket(ticket_id)

        print("Ticket deleted successfully")


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    asyncio.run(test_crud())
    profiler.disable()


    stream = io.StringIO()

    stats = pstats.Stats(
        profiler,
        stream=stream
    )

    stats.strip_dirs()

    stats.sort_stats("cumulative")

    stats.print_stats(50)

    print("\n")
    print("=" * 80)
    print("CPROFILE RESULTS")
    print("=" * 80)

    print(stream.getvalue())


if __name__ == "__main__":
    main()