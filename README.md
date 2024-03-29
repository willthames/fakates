# fakates

fakates is a fake service for Kubernetes

The primary motivation is to use our existing Kubernetes configuration management
to test what resources will be updated when the configuration source code changes.

Obviously there are a number of alternative approaches but the aim is to avoid
any pods actually needing to run in the test phase.

If you use this with ansible and `wait`, you'll want to set wait to `false` as
none of the wait expectations will ever be met!

# Usage

```
pip install -r requirements.txt
python run.py [--database /path/to/db.json] [--port 5000] [--host 127.0.0.1]
kubectl config set-cluster fakates --server http://localhost:5000
kubectl config set-context fakates --cluster fakates
kubectl config use-context fakates
kubectl create -f examples/service.yml
kubectl get svc -n test
ansible -m k8s_facts -a 'kind=Service namespace=test' localhost
```

# Troubleshooting

`kubectl` is the easiest way to see what is going wrong if you're getting weird
responses back - `kubectl -v8 ...` shows all the API calls and responses

The contents of the database are also likely helpful `jq .  /tmp/db.json` to see
whether resources are actually defined correctly

# Not implemented

## Next on the list
[ ] `label-selectors` (half done - `notin`, `!label` and `label != X` are not working
    for resourecs with no labels)
[ ] `watch` - https://kubernetes.io/docs/reference/using-api/api-concepts/#efficient-detection-of-changes

## As needed
* `as=Table` - https://kubernetes.io/docs/reference/using-api/api-concepts/#receiving-resources-as-tables
* `limit`
* `field-selectors`
* `merge` types (particularly strategic, which will be hard)
* anything other than `GET` on `List`s
