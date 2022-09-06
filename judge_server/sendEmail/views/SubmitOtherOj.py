from django.http import JsonResponse, HttpResponse

# from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from match_system.src.match_server.match_server import Match


def operate(sid, tid):
    # Make socket
    transport = TSocket.TSocket('10.0.38.113', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Match.Client(protocol)

    # Connect!
    transport.open()
    # transport = TFramedTransport(TSocket('10.0.38.113', 9090))
    # protocol = TCompactProtocol.TCompactProtocol(transport)
    # client = Hbase.Client(protocol)
    # transport.open()

    client.add_player(sid, tid)

    # Close!
    transport.close()


def SubmitOtherOj(request):
    data = request.POST
    sid = data.get('sid')
    tid = data.get('tid')
    sid = int(sid)
    tid = int(tid)
    operate(sid, tid)

    return JsonResponse({
        'msg': "success",
    })
