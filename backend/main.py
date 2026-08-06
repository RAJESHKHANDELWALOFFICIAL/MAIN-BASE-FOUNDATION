from backend.core.bootstrap import Bootstrap


def main():

    print("=" * 60)
    print("MAIN BASE FOUNDATION")
    print("=" * 60)

    bootstrap = Bootstrap()

    system = bootstrap.boot()

    print(system)

    print("=" * 60)
    print("SYSTEM STARTED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
