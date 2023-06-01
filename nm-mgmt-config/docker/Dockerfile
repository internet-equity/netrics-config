FROM golang:1.20 AS build-stage

WORKDIR /

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build nm-mgmt-config.go

# Run the tests in the container
#FROM build-stage AS run-test-stage
#RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=busybox:1.36.1-uclibc /bin/sh /bin/sh
COPY --from=busybox:1.36.1-uclibc /bin/sleep /bin/sleep
COPY --from=build-stage /nm-mgmt-config /nm-mgmt-config
COPY nm-mgmt-config.sh /

#EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/bin/sh", "./nm-mgmt-config.sh"]
