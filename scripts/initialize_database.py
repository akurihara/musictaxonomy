from musictaxonomy.auth import models as auth_models  # noqa: F401
from musictaxonomy.database import Base, engine
from musictaxonomy.graph import models as graph_models  # noqa: F401


def main():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
