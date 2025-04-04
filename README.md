# Web service example for 1259

To generated a pickled k-means model, run:

```bash
uv run model.py
```

To launch the API, run (in the `src` folder):

```bash
uv run fastapi dev
```

Open API documentation is available at `/docs`.

We can consider the specification for an "average" penguin to be:

```json
[
  {
    "flipperLength": 201.5,
    "billLength": 45.4,
    "billDepth": 17.3
  }
]
```

To predict the cluster for a new penguin, use:

```
curl -X "POST" "http://localhost:8000/" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'[
  {
    "flipperLength": 201.5,
    "billLength": 45.4,
    "billDepth": 17.3
  }
]'
```