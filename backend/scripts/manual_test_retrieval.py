from app.db.session import SessionLocal
from app.services.retrieval_service import retrieve_similar_chunks


db = SessionLocal()


question = "What happens when an employee is sick?"


results = retrieve_similar_chunks(
    question,
    db,
)


print(
    f"Found {len(results)} chunks\n"
)


for chunk in results:

    print("=" * 60)

    print(chunk.content)

    print()
    

db.close()