# Observation row shape

An observation is a dated row against a crop. A row that cannot fill the
required fields is a note. It does not enter the crop record.

The machine schema is [`data/schema/observation.schema.json`](../data/schema/observation.schema.json).

## Required fields

| Field | Meaning |
|---|---|
| `observation_id` | `obs-YYYY-NNNN` |
| `crop_id` | Stable crop identifier (`basil`, `radish_rambo`, …) |
| `provenance` | `thh_observation`, `thh_trial`, `kit_buyer`, `partner_observation`, `supplier_spec`, `horticultural_consensus`, `external_study`, or `working_recommendation` |
| `observer_class` | `house`, `kit_buyer`, `partner`, or `supplier` |
| `sow_date` | ISO date |
| `medium` | What it grew in |
| `lamp` | Whether a lamp was used |
| `as_of` | When the row was written |
| `source` | Where the numbers came from |
| `status` | `draft`, `accepted`, or `rejected` |

Useful optional fields: `first_cut_date`, `first_cut_days`, `yield_g`,
`failure_mode`, `aspect`, `latitude_band`, `location_note` (city or region,
never a street address), `kit`, `variety_name`.

`partner_id` is internal only. It must never be printed on a treatise.

## Public rule

Public pages show conditions, not people. A partner row stamps
`partner_observation` plus medium, lamp, aspect, and latitude band. It does
not stamp a firm, a grower, or a logo.

## What is not in this repository

v0.1 publishes the shape, not a ledger of partner rows, and not a recruitment
or order-of-approach playbook. Those stay in private operations.
