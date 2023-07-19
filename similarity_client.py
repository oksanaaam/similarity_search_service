import grpc
import similarity_pb2
import similarity_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:5001")
    stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)

    add_item_request = similarity_pb2.AddItemRequest(id="6", description="ssss item")
    add_item_response = stub.AddItem(add_item_request)
    print("Add Item Response:", add_item_response)

    search_items_request = similarity_pb2.SearchItemsRequest(query="sss")
    search_items_response = stub.SearchItems(search_items_request)
    print("Search Items Response:", search_items_response.search_id)

    if search_items_response.search_id:
        get_search_results_request = similarity_pb2.GetSearchResultsRequest(
            search_id=search_items_response.search_id
        )
        get_search_results_response = stub.GetSearchResults(get_search_results_request)
        if get_search_results_response.results:
            print("Get Search Results Response:", get_search_results_response)
        else:
            print("No search results found.")
    else:
        print("Cannot retrieve search results.")


if __name__ == "__main__":
    run()
