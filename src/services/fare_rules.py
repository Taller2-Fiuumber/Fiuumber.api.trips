from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


def get_selected_fare(mongo_client):
    database = mongo_client[DB_NAME]

    selected_rule = database["fare_rules"].find_one({"selected": True})

    if selected_rule is not None:
        return selected_rule
    return None


def create_fare_rule(mongo_client, fare_rule):
    database = mongo_client[DB_NAME]

    print("_____________fare_rules", fare_rule)
    new_fare_rule = database["fare_rules"].insert_one(fare_rule)
    print("_____________new_fare_rules", new_fare_rule)

    created_new_fare_rule = database["fare_rules"].find_one(
        {"_id": new_fare_rule.inserted_id}
    )

    print("_____________created_new_fare_rule", created_new_fare_rule)

    if created_new_fare_rule is not None:
        return created_new_fare_rule
    return None


def list_fare_rules(mongo_client):
    database = mongo_client[DB_NAME]

    fare_rules = database["fare_rules"].find()
    return list(fare_rules)


def find_fare_rules_by_id(id: str, mongo_client):
    database = mongo_client[DB_NAME]

    if (fare_rule := database["fare_rules"].find_one({"_id": id})) is not None:
        return fare_rule
    return None


def select_a_fare_rule(id: str, mongo_client):
    database = mongo_client[DB_NAME]

    old_selected_fare_rule = database["fare_rules"].find_one({"selected": True})
    new_selected_fare_rule = database["fare_rules"].update_one(
        {"_id": id}, {"$set": {"selected": True}}
    )

    if new_selected_fare_rule is not None:
        if old_selected_fare_rule is not None:
            database["fare_rules"].update_one(
                {"_id": old_selected_fare_rule["_id"]}, {"$set": {"selected": False}}
            )
        return database["fare_rules"].find_one({"_id": id})
    return None
