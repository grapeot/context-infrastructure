## 元数据

- **类型**: Workflow
- **分类**: Infrastructure & DevOps
- **适用场景**: Deploy applications to Kubernetes — Deployments, Services, Ingress, ConfigMaps, Secrets, health checks, and scaling.
- **上游来源**: [kubernetes-deploying](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/kubernetes-deploying)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Kubernetes Deploying

Deploy and manage applications on Kubernetes.

## Core Resources

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-registry/my-app:v1.2.3
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: my-app-secrets
                  key: database-url
            - name: NODE_ENV
              value: production
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: my-app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app
                port:
                  number: 80
```

### ConfigMap & Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-app-config
data:
  LOG_LEVEL: info
  FEATURE_FLAGS: '{"darkMode": true}'
---
apiVersion: v1
kind: Secret
metadata:
  name: my-app-secrets
type: Opaque
stringData:
  database-url: postgresql://user:pass@host:5432/db
  api-key: sk-abc123
```

## Common Commands

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl rollout status deployment/my-app

# View pods
kubectl get pods -l app=my-app

# View logs
kubectl logs -f deployment/my-app

# Execute into a pod
kubectl exec -it <pod-name> -- /bin/sh

# Scale
kubectl scale deployment/my-app --replicas=5

# Rollback
kubectl rollout undo deployment/my-app

# Port forward for local debugging
kubectl port-forward svc/my-app 3000:80
```

## Deployment Strategies

| Strategy | How | When |
|----------|-----|------|
| Rolling update (default) | Replace pods one at a time | Most deployments |
| Recreate | Kill all old pods, start new ones | When you can't run two versions simultaneously |
| Blue/green | Run two full environments, switch traffic | Need instant rollback |
| Canary | Route small % of traffic to new version | High-risk changes |

Rolling update config:
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

## Health Checks

Always set both:
- **livenessProbe**: "Is the process healthy?" — restarts the pod if it fails
- **readinessProbe**: "Can it handle traffic?" — removes from service if it fails

Common probe types:
- `httpGet`: Hit an HTTP endpoint (most common)
- `exec`: Run a command in the container
- `tcpSocket`: Check if a port is open

## Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Tips

- Always set resource requests and limits
- Use namespaces to isolate environments (`dev`, `staging`, `prod`)
- Never put secrets in plaintext YAML committed to git — use Sealed Secrets, SOPS, or external secret managers
- Tag images with specific versions, never use `:latest` in production
- Set `PodDisruptionBudget` for high-availability workloads
