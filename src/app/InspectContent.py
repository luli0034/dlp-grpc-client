import grp
import grpc
import dlpcontainer_pb2 as pb2
import dlpcontainer_pb2_grpc as pb2_grpc

class RunInspectContent:

    def __init__(self, grpc_server):
        self.server=grpc_server

    def set_info_types(self, info_types):
        self.inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    
    def run(self, inspect_content):
        # Start request and get response from grpc server
        with grpc.insecure_channel(self.server) as conn:
            stub = pb2_grpc.DlpServiceStub(channel=conn)
            response = stub.InspectContent(
                self._get_request_class(inspect_content)
            )
        inspect_results = self._format_response(response)
        return inspect_results

    def _get_request_class(self, inspect_content):
        if not self.inspect_config:
            raise ValueError("Infotypes should be build before run.")
        # Construct request
        request = pb2.InspectContentRequest(
            item=self._content_to_item(inspect_content),
            inspect_config=self.inspect_config
        )
        return request

     # Construct item
    def _content_to_item(self, inspect_content):
        return {"value": inspect_content}


    def _format_response(self, response):
        assert isinstance(response,pb2.InspectContentResponse)
        inspect_results=[]
        findings = response.findings
        if len(findings) > 0:
            for finding in findings:
                inspect_results.append(self._get_inspect_result(
                        info_type=finding.info_type.name, 
                        start_idx=finding.byte_offset, 
                        end_idx=(finding.byte_offset+finding.byte_length), 
                        quote=finding.quote
                    )
                )
        return inspect_results
    def _get_inspect_result(self, info_type, start_idx, end_idx, quote):
        return {
            "info_type":info_type,
            "start_idx":start_idx,
            "end_idx":end_idx,
            "context":quote
        }

class RunDeidentifyContent:

    def __init__(self, grpc_server):
        self.server=grpc_server
        

    def set_info_types(self, info_types):
        self.inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}
        self._set_deidentify_config()

    def _set_deidentify_config(self):
        self.deidentify_config=pb2.DeidentifyConfig(
            info_type_transformations={
                "transformations":[
                    {
                        "primitive_transformation": {"replace_with_info_type_config":{}},
                        "info_types": self.inspect_config["info_types"]
                    }
                ]
            }
        )
        # self.deidentify_config = {
        #     "info_type_transformations": {
        #         "transformations": [
        #             {
        #                 "primitive_transformation": {"replace_with_info_type_config":{}},
        #                 "info_types": [
        #                     {"name": 'PERSON_NAME'}
        #                 ]
        #             }
        #         ]
        #     }
        # }

    
    def run(self, inspect_content):
        # Start request and get response from grpc server
        with grpc.insecure_channel(self.server) as conn:
            stub = pb2_grpc.DlpServiceStub(channel=conn)
            response = stub.DeidentifyContent(
                self._get_request_class(inspect_content)
            )
        return response

    def _get_request_class(self, inspect_content):
        if not self.inspect_config:
            raise ValueError("Infotypes should be build before run.")
        # Construct request
        request = pb2.DeidentifyContentRequest(
            item=self._content_to_item(inspect_content),
            deidentify_config=self.deidentify_config,
            inspect_config=self.inspect_config
        )
        return request

     # Construct item
    def _content_to_item(self, inspect_content):
        return {"value": inspect_content}