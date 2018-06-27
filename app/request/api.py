import uuid

from flask import abort, jsonify, make_response, request
from flask.views import MethodView

from app.auth.decoractor import token_required
from app.models import Request


class RequestAPI(MethodView):
    """This class-based view for requesting a ride."""
    decorators = [token_required]
    def post(self,current_user, ride_id):
        if ride_id:
            try:
                request = Request()
                passenger = current_user[2]
                all_reqs = request.fetch_all()
                for req in  all_reqs:
                    req= {"Id":req['Id'],"ride":req['ride'],"passenger":req['passenger']}
                    if req in all_reqs:
                        return jsonify({'msg': 'You already requested to join this ride' }), 409
                    else:
                        request.insert(ride_id, passenger)  
                        return jsonify({'msg': 'A request to join this ride has been sent' }), 201 
            
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

    def get(self, current_user, ride_id):
        '''Gets all requests''' 
        try:
            request = Request()
            requests = request.fetch_all()
            if requests == []:
                return jsonify({"msg": "You haven't recieved any ride requests yet"}), 200
            return jsonify(requests), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500
   
    def put(self,current_user, ride_id, request_id):
        """Accept or reject a ride request"""
        data = request.get_json()
        if data['status']=='accepted' or data['status'] =='rejected':
            try:
                req=Request(id=request_id,ride_id = ride_id)
                req.update_request(request_id,data)
                response = {
                'message':'you have {} this ride request'.format(data['status'])
                }
                return make_response(jsonify(response)), 200
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500
        response = {
            'message':'The status can only be in 3 states, requested, accepted and rejected'
        }
        return make_response(jsonify(response)), 401
