from backend.identity.service import IdentityService


def main():
    service = IdentityService()

    identity = service.create_demo_identity()

    print("MAIN BASE FOUNDATION")
    print("---------------------")
    print(identity)


if __name__ == "__main__":
    main()
