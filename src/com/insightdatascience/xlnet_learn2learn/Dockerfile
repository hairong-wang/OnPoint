# Use tensorflow as base image
# Model checkpoint
# Training scripts
# Training dataset



FROM golang:1.8-alpine
ADD . /go/src/hello-app
RUN go install hello-app

FROM alpine:latest
COPY --from=0 /go/bin/hello-app .
ENV PORT 8080
CMD ["./hello-app"]




wget https://storage.googleapis.com/xlnet/released_models/cased_L-24_H-1024_A-16.zip
