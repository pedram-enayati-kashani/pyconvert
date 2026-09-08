from threading import local

_thread_locals = local()

def get_current_model_info():
    return getattr(_thread_locals, 'model_info', None)

class CKEditorMetadataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Read the headers we set in JavaScript
        model_name = request.headers.get('X-Model-Name')
        object_id = request.headers.get('X-Object-Id')

        if model_name and object_id:
            _thread_locals.model_info = {
                'model': model_name,
                'id': object_id
            }
        else:
            _thread_locals.model_info = None

        response = self.get_response(request)
        return response
