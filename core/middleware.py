import time
import logging
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

class PerformanceMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timing
        start_time = time.time()
        
        # Count initial queries
        initial_queries = len(connection.queries)
        
        # Process request
        response = self.get_response(request)
        
        # Calculate performance metrics
        end_time = time.time()
        request_time = end_time - start_time
        final_queries = len(connection.queries)
        query_count = final_queries - initial_queries
        
        # Log slow requests (over 1 second)
        if request_time > 1.0:
            logger.warning(
                f"Slow request: {request.path} took {request_time:.2f}s "
                f"with {query_count} queries"
            )
        
        # Log excessive queries (over 20 queries)
        if query_count > 20:
            logger.warning(
                f"High query count: {request.path} made {query_count} queries "
                f"in {request_time:.2f}s"
            )
        
        # Add performance headers in development
        if settings.DEBUG:
            response['X-Request-Time'] = f"{request_time:.3f}s"
            response['X-Query-Count'] = str(query_count)
        
        return response

class QueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        
        # Log queries in development
        if settings.DEBUG and hasattr(settings, 'LOG_QUERIES') and settings.LOG_QUERIES:
            for query in connection.queries:
                if float(query['time']) > 0.1:  # Log queries taking more than 100ms
                    logger.info(
                        f"Slow query ({query['time']}s): {query['sql'][:200]}..."
                    )
        
        return response 