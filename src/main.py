import grpc
import dlpcontainer_pb2 as pb2
import dlpcontainer_pb2_grpc as pb2_grpc
from app.InspectContent import RunInspectContent, RunDeidentifyContent
def run():
    info_types = ["EMAIL_ADDRESS", "PERSON_NAME"]
    input_str = "Hello I am Luli, She is my sister, Tracy!!!"
    inspect_content = RunInspectContent('localhost:50051')
    inspect_content.set_info_types(info_types)
    inspect_results = inspect_content.run(input_str)

    # deidentifier = RunDeidentifyContent('localhost:50051')
    # deidentifier.set_info_types(info_types)
    # response = deidentifier.run("Hello my name is Melissa!!!")
    


    print(inspect_results)


if __name__ == '__main__':
    run()