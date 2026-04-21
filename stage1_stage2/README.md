#  HNG Stage 1&2 Backend – Intelligence Query Engine

##  Overview

This project is a demographic intelligence API built for Insighta Labs. It allows clients to filter, sort, paginate, and query demographic profile data efficiently, including support for natural language queries.

The system is built with Flask and uses a seeded dataset of 2026 profiles.

---

##  Features

### ✅ 1. Advanced Filtering

Supports combining multiple filters:

* `gender`
* `age_group`
* `country_id`
* `min_age`, `max_age`
* `min_gender_probability`
* `min_country_probability`

Example:

```
/api/profiles?gender=male&country_id=NG&min_age=25
```

---

###  2. Sorting

* `sort_by`: `age`, `created_at`, `gender_probability`
* `order`: `asc`, `desc`

Example:

```
/api/profiles?sort_by=age&order=desc
```

---

###  3. Pagination

* `page` (default: 1)
* `limit` (default: 10, max: 50)

Example:

```
/api/profiles?page=2&limit=10
```

---

###  4. Natural Language Search (Core Feature)

Endpoint:

```
GET /api/profiles/search?q=<query>
```

---

##  Natural Language Parsing Approach

The system uses a **rule-based parser** (no AI/LLMs) to convert plain English queries into structured filters.

###  Supported Keywords & Mapping

| Phrase              | Interpretation             |
| ------------------- | -------------------------- |
| "male", "males"     | `gender=male`              |
| "female", "females" | `gender=female`            |
| "young"             | `min_age=16`, `max_age=24` |
| "adult"             | `age_group=adult`          |
| "teenager"          | `age_group=teenager`       |
| "child"             | `age_group=child`          |
| "senior"            | `age_group=senior`         |
| "above X"           | `min_age=X`                |
| "below X"           | `max_age=X`                |
| "from <country>"    | maps to `country_id`       |

###  Country Mapping

Country names are mapped manually to ISO codes, e.g.:

* nigeria → NG
* kenya → KE
* angola → AO

---

###  Example Queries

| Query                    | Parsed Filters                              |
| ------------------------ | ------------------------------------------- |
| "young males"            | gender=male, age 16–24                      |
| "females above 30"       | gender=female, min_age=30                   |
| "people from nigeria"    | country_id=NG                               |
| "adult males from kenya" | gender=male, age_group=adult, country_id=KE |

---

###  Invalid Queries

Unrecognized queries return:

```json
{
  "status": "error",
  "message": "Unable to interpret query"
}
```

---

##  Limitations

* Only supports predefined keywords and patterns
* Cannot handle complex sentences or grammar variations
* Country mapping is limited to known values
* Does not support synonyms (e.g., "guys" instead of "males")
* Cannot interpret multiple numeric conditions beyond simple "above/below"
* Queries must follow expected structure for correct parsing

---

##  Database

The database contains **2026 seeded profiles** with the following structure:

* UUID v7 primary key
* Name (unique)
* Gender + probability
* Age + age group
* Country ID + name + probability
* Timestamp (UTC ISO 8601)

---

##  API Base URL

```
https://your-app-url/api
```

---

##  Testing

All endpoints were tested using:

* Postman
* Browser
* cURL

---

##  Notes

* All timestamps are in UTC ISO 8601 format
* CORS is enabled for all origins
* Duplicate records are prevented during seeding
* Query parameters are validated to avoid invalid input

---

##  Conclusion

This API provides a fast and flexible way to query demographic data, supporting both structured and natural language queries while maintaining performance and simplicity.
