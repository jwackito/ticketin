# event-catalog Specification

## Purpose
Provide a public, read-only view of published upcoming events so visitors can discover what is happening and inspect an individual event.

## Requirements

### Requirement: Event representation

Each event returned by the API SHALL expose `id`, `title`, `description`, `venue`, `starts_at`, `capacity`, `status`, `created_at`, and `updated_at`. `description` MAY be null; all other fields SHALL be present.

#### Scenario: Event fields are present

- **WHEN** an event is returned in a list or detail response
- **THEN** the response contains `id`, `title`, `description`, `venue`, `starts_at`, `capacity`, `status`, `created_at`, and `updated_at`

### Requirement: List published upcoming events

The system SHALL return only events whose status is `published` and whose `starts_at` is at or after the current time, ordered by `starts_at` ascending with `id` as a deterministic tie-breaker.

#### Scenario: Draft events are excluded

- **WHEN** the catalog contains a draft event and a published event
- **THEN** the list response contains only the published event

#### Scenario: Past events are excluded

- **WHEN** the catalog contains a published event whose `starts_at` is in the past
- **THEN** the list response does not contain that event

#### Scenario: Events are ordered by start time

- **WHEN** the catalog contains multiple published upcoming events
- **THEN** the list response orders them by `starts_at` ascending, using `id` ascending when start times are equal

### Requirement: Paginate the event list

The system SHALL paginate the event list with `limit` and `offset` query parameters and SHALL return the page items together with the total number of matching events. The default `limit` SHALL be 20 and the default `offset` SHALL be 0.

#### Scenario: Default page

- **WHEN** a client requests the event list without `limit` or `offset`
- **THEN** the response contains at most 20 items, `limit` is 20, `offset` is 0, and `total` is the total number of matching events

#### Scenario: Explicit page

- **WHEN** a client requests the event list with a valid `limit` and `offset`
- **THEN** the response contains at most `limit` items starting after `offset` matching events, and echoes both values

#### Scenario: Offset past the end

- **WHEN** a client requests an `offset` greater than or equal to `total`
- **THEN** the response contains an empty `items` array and the correct `total`

#### Scenario: Empty catalog

- **WHEN** there are no published upcoming events
- **THEN** the response contains an empty `items` array and `total` is 0

### Requirement: Validate pagination parameters

The system SHALL reject a `limit` less than 1 or greater than 100, and an `offset` less than 0, with HTTP status 422.

#### Scenario: Limit outside the allowed range

- **WHEN** a client requests the event list with `limit` of 0 or 101
- **THEN** the system responds with HTTP 422

#### Scenario: Negative offset

- **WHEN** a client requests the event list with a negative `offset`
- **THEN** the system responds with HTTP 422

### Requirement: Retrieve a published event by id

The system SHALL return a published event by id regardless of whether the event has already started. Draft events and unknown ids SHALL both return HTTP 404 with the same error detail.

#### Scenario: Published event is returned

- **WHEN** a client requests the id of a published event
- **THEN** the system responds with HTTP 200 and the event

#### Scenario: Past published event is still returned

- **WHEN** a client requests the id of a published event whose `starts_at` is in the past
- **THEN** the system responds with HTTP 200 and the event

#### Scenario: Draft event is not found

- **WHEN** a client requests the id of a draft event
- **THEN** the system responds with HTTP 404 and the same error detail as an unknown id

#### Scenario: Unknown id is not found

- **WHEN** a client requests an id that does not exist
- **THEN** the system responds with HTTP 404 and the same error detail as a draft id

#### Scenario: Malformed id is rejected

- **WHEN** a client requests an id that is not a valid UUID
- **THEN** the system responds with HTTP 422
