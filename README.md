# eKart mini DevOps project

A tiny Flask shopping catalogue designed for a GitHub → Quay.io → OpenShift CI/CD exercise.

## 1. Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://localhost:8080, http://localhost:8080/api/products and http://localhost:8080/health.

## 2. Build and push to Quay

Create a public repository named `ekart` at https://quay.io.
Replace `YOUR_QUAY_USERNAME` in `openshift/deployment.yaml`.

```bash
docker build -t quay.io/YOUR_QUAY_USERNAME/ekart:latest .
docker login quay.io
docker push quay.io/YOUR_QUAY_USERNAME/ekart:latest
```

Use a Quay robot account/token for automation where possible. Never commit credentials.

## 3. Deploy to Developer Sandbox

Log in to the OpenShift web console, open the Web Terminal (or use `oc` locally after downloading the login command), and select your project:

```bash
oc project
oc apply -f openshift/deployment.yaml
oc apply -f openshift/service-route.yaml
oc get pods
oc get route ekart
```

If the Quay repository is private, create a pull secret and link it to the default service account:

```bash
oc create secret docker-registry quay-pull   --docker-server=quay.io   --docker-username='YOUR_QUAY_USERNAME'   --docker-password='YOUR_QUAY_TOKEN'   --docker-email='YOUR_EMAIL'
oc secrets link default quay-pull --for=pull
```

For a public Quay repository, the pull secret is not needed.

## 4. Configure the Tekton pipeline

The `pipeline/pipeline.yaml` expects the `git-clone`, `buildah`, and `openshift-client` Tasks to already exist in the namespace. Check first:

```bash
oc get tasks
oc get pipelines
```

If those Tasks are missing, use the OpenShift Pipelines catalog or the Tasks provided by your cluster administrator; do not assume you can install cluster-wide components in the shared sandbox.

Create a workspace PVC (the cluster may enforce storage quota):

```bash
oc create pvc ekart-workspace --access-modes=ReadWriteOnce --resources=requests.storage=1Gi
```

Create a Quay auth secret from a Quay robot account/token. Tekton's Buildah task expects a Docker config file at `.dockerconfigjson` or a `config.json` in the dockerconfig workspace, depending on the installed Task version. One common setup is:

```bash
oc create secret docker-registry quay-auth   --docker-server=quay.io   --docker-username='YOUR_QUAY_USERNAME'   --docker-password='YOUR_QUAY_TOKEN'   --docker-email='YOUR_EMAIL'
```

Mount that secret as a workspace in the PipelineRun (see the note below), or configure the Buildah Task's `dockerconfig` workspace to read the secret. Do not put tokens in Git.

Apply the pipeline:

```bash
oc apply -f pipeline/pipeline.yaml
```

Then create a PipelineRun from the Pipelines page in the OpenShift console, supplying:
- `git-url`: your GitHub repository HTTPS URL
- `git-revision`: `main`
- `image`: `quay.io/YOUR_QUAY_USERNAME/ekart`
- `shared-workspace`: the `ekart-workspace` PVC
- `quay-auth`: a workspace backed by your Quay auth secret

The exact Task names, workspace names, and secret mounting format can vary by installed OpenShift Pipelines version. Inspect with `oc get tasks` and `oc describe task buildah` before running. The pipeline is a learning starter, not a guaranteed drop-in for every sandbox namespace.

## 5. CI/CD flow

GitHub source → `git-clone` → Buildah build → push to Quay → `oc set image` → rollout status.

## Notes

- Developer Sandbox is a shared, time-limited learning environment. Export your source code and manifests to GitHub.
- Keep the Quay image public for the simplest first deployment, or configure pull credentials for a private repository.
- The image tag `latest` is used to keep the first exercise simple. For a stronger pipeline, use the Git commit SHA as an immutable image tag.
