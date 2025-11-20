{{/*
Common template helpers used throughout the chart
*/}}

{{- define "sports-store-app.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- $fullname := printf "%s-%s" .Release.Name $name -}}
{{- if gt (len $fullname) 63 -}}
{{- $fullname := printf "%s" (trunc 63 $fullname) -}}
{{- end -}}
{{- $fullname | trimSuffix "-" -}}
{{- end -}}

{{- define "sports-store-app.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{ include "sports-store-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "sports-store-app.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}