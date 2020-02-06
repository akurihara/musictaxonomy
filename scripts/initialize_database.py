from musictaxonomy.auth import models as auth_models  # noqa: F401
from musictaxonomy.database import Base, Session, engine
from musictaxonomy.graph import models as graph_models  # noqa: F401


def main():
    Base.metadata.create_all(engine)

    session = Session()
    session.add(graph_models.MainGenre(id=1, spotify_name="pop", display_name="Pop"))
    session.add(graph_models.MainGenre(id=2, spotify_name="rock", display_name="Rock"))
    session.add(
        graph_models.MainGenre(id=3, spotify_name="hip hop", display_name="Hip Hop")
    )
    session.add(graph_models.MainGenre(id=4, spotify_name="jazz", display_name="Jazz"))
    session.add(graph_models.MainGenre(id=5, spotify_name="folk", display_name="Folk"))
    session.add(
        graph_models.MainGenre(id=6, spotify_name="country", display_name="Country")
    )
    session.add(
        graph_models.MainGenre(id=7, spotify_name="edm", display_name="Electronic")
    )
    session.add(
        graph_models.MainGenre(id=8, spotify_name="classical", display_name="Classical")
    )
    session.add(
        graph_models.MainGenre(id=9, spotify_name="blues", display_name="Blues")
    )
    session.add(
        graph_models.MainGenre(id=10, spotify_name="reggae", display_name="Reggae")
    )
    session.add(graph_models.MainGenre(id=11, spotify_name="r&b", display_name="R&B"))

    session.commit()


if __name__ == "__main__":
    main()
