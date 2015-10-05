## Definitions

In order to clearly understand the terms used throughout the rest of this document as well
as other EchoChamber documentation, refer to the following set of definitions for terminology.

### EchoChamber

> The entire phrase `EchoChamber` refers to this entire suite of software.

### Chamber

> The `Chamber server`, or just `Chamber`, is the central server-software that handles
> configurations, runs test code, simulates a network, and manages clients.
> It presents a REST-like API for client communication as well as test configuration.

### Echo

> `Echo`, sometimes referred to as the `Echo API`, is the API presented to users of this
> software for the purposes of configuring and running tests.  The phrase `Echo Library`
> may also be used to refer to any library implementations to cover the Echo API.


# Notation

HTTP requests will be described with a single line of the format
`method /full/path {key1: value1, key2: value2, ..., keyN: valueN}`.
Where

`method` is an HTTP method such as GET, POST, PUT, DELETE, etc...

`/full/path` is a URI path with a generic query string in some cases,
such as `/send` or `/receive/from?id=<id: number>&before=<date: string>`.

The final value is a JSON representation of the POST parameters (if any) expected.
For example, `{"id": <id: number>, "before": <date: string>}`

You will notice that parameters to both a URI's query string as well as a POST-like
request's data fields, values are represented in the format `<name: type>` where the name
can be arbitrary and the type will be a JSON type (number, string, object, array, boolean).

In the case of an array, the type wil be specified `[type]`, where type is again another type.
For example, an array of numbers would be represented as `<numbers: [number]>`.
An object would be represented like `<values: {key1: type, key2: type, ..., keyN: type}>`.

Note that in some cases, rather than providing a type, a constant will be used in a description.
For example, if a request or response is expected to have a `success` field that is always true
in a particular circumstance, it will be described as `{success: true}`.
