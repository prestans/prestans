# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Eternity Technologies nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ETERNITY TECHNOLOGIES BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#:
#: This file mostly contains constants for HTTP
#:

class VERB:

    #:
    #: Encapsulates HTTP Verbs supported by the prestans framework in accordance
    #: with the REST definition. Each prestans REST handler must supporto at least
    #: one HTTP verb.
    #:

    GET    = "GET"
    POST   = "POST"
    PUT    = "PUT"
    PATCH  = "PATCH"
    DELETE = "DELETE"

class STATUS:

    #:
    #: The following is a selection of HTTP status codes that are recommended for use 
    #: by REST services. You are welcome to use other available status codes.
    #:

    OK                      = 200
    CREATED                 = 201
    ACCEPTED                = 202
    NO_CONTENT              = 204
    NOT_MODIFIED            = 304
    BAD_REQUEST             = 400
    UNAUTHORIZED            = 401
    FORBIDDEN               = 403
    NOT_FOUND               = 404
    CONFLICT                = 409
    GONE                    = 410
    INTERNAL_SERVER_ERROR   = 500
    SERVICE_UNAVAILABLE     = 503