# web-server-from-scratch
A web server following the WSGI standards from scratch.

The goal of this short project was to gain a better understanding of how HTTP servers work as well as WSGI, as I previously only thought of it as a black box, and I wasn't aware of how application servers fit into the picture.

## Walkthrough:

# web_server

This directory contains all the important components in the server such as handling HTTP connections, loading resources, and etc. The HttpServer class can be run to only serve static files or it can connect with a WSGI application.

# applications

This directory contains a base Application class as well as a MockApplication class which are application callables that can be attached to the HttpServer to handle requests.

# public

A directory holding static files to be served to clients

# tests

It could be a little more developed. However, as of right now there is a test for WSGI conformity as well as a test for a simple static server request.
