import zmq
import time
import json
from client.diabetes_extremely_simplified_model_builder_with_offline_evaluator import prepare_model

if __name__ == '__main__':
    port = 5555
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind(f"tcp://*:{port}")

    while True:
        print("Job executor is waiting for a new job request.")
        msg = socket.recv()
        print("Job executor has received a new job request.")
        msg_dict = json.loads(msg.decode('ascii'))
        print(msg_dict)
        msg_dict_value = msg_dict["job_ID"]
        print(msg_dict_value)
        print("Job execution is starting.")
        try:
            prepare_model()
        except:
            msg_content_dict = {}
            msg_content_dict["error"] = -1
            msg_content = str(json.dumps(msg_content_dict))
            msg_string = msg_content.encode('ascii')
            socket.send(msg_string)
        print("Job is completed.")
        print("Job executor is about to report the completion of the job back to the requester.")
        msg_content_dict = {}
        msg_content_dict["some_other_key"] = msg_dict_value
        msg_content = str(json.dumps(msg_content_dict))
        msg_string = msg_content.encode('ascii')
        socket.send(msg_string)
