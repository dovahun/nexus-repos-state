{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "rabbitmq-update-definitions.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "rabbitmq-update-definitions.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "rabbitmq-update-definitions.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "rabbitmq-update-definitions.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "rabbitmq-update-definitions.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Generate chart secret name
*/}}
{{- define "rabbitmq-update-definitions.secretName" -}}
{{ default (include "rabbitmq-update-definitions.fullname" .) .Values.existingSecret }}
{{- end -}}

{{/*
Generate chart ssl secret name
*/}}
{{- define "rabbitmq-update-definitions.certSecretName" -}}
{{ default (print (include "rabbitmq-update-definitions.fullname" .) "-cert") .Values.rabbitmqCert.existingSecret }}
{{- end -}}

{{/*
Defines a JSON file containing definitions of all broker objects (queues, exchanges, bindings, 
users, virtual hosts, permissions and parameters) to load by the management plugin.
*/}}
{{- define "rabbitmq-update-definitions.definitions" -}}
  {{- $global_parameters := .Files.Get "ci/global_parameters.yaml" | fromYaml -}}
  {{- $users := .Files.Get "ci/users.yaml"| fromYaml -}}
  {{- $vhosts := .Files.Get "ci/vhosts.yaml" | fromYaml  -}}
  {{- $permissions := .Files.Get "ci/permissions.yaml"| fromYaml  -}}
  {{- $parameters := .Files.Get "ci/parameters.yaml" | fromYaml  -}}
  {{- $policies := .Files.Get "ci/policies.yaml" | fromYaml -}}
  {{- $queues := .Files.Get "ci/queues.yaml"| fromYaml -}}
  {{- $exchanges := .Files.Get "ci/exchanges.yaml"| fromYaml -}}
  {{- $bindings := .Files.Get "ci/bindings.yaml"| fromYaml -}}
  {{- $merged := merge $global_parameters $users $vhosts $permissions $parameters $policies $queues $exchanges $bindings -}}
  {{ $merged | toPrettyJson }}
{{- end -}}