# Deployment Rollback and Recovery Guide

This guide describes rollback procedures for the containerized ECS Fargate and non-containerized EC2 deployment approaches.

> These are documented recovery procedures. They have not been tested against a live AWS deployment.

## 1. ECS Fargate Rollback

### When to Roll Back

- Application health checks fail after deployment.
- Frontend or backend returns unexpected errors.
- New application version introduces a critical regression.

### Procedure

1. Identify the last healthy ECS task definition revision in the AWS ECS console or CLI.
2. Update the affected ECS service to use that previous task definition revision.
3. Wait for the ECS service to stabilize.
4. Confirm ALB target health and application endpoint responses.
5. Review CloudWatch logs to investigate the failed deployment.

Example:

```bash
aws ecs update-service \
  --cluster <cluster-name> \
  --service <service-name> \
  --task-definition <previous-task-definition-arn> \
  --region ap-south-1
```

Replace placeholders with the actual deployed resource names and revision.

**Important:** Use immutable image tags or digests so an earlier task definition references the intended application image.

## 2. EC2 Rollback

The EC2 approach uses an Auto Scaling Group with application installation configured through user data.

### Procedure

1. Identify the previous known-good application commit or release.
2. Restore the previous application version in the EC2 provisioning configuration.
3. Create a new launch template version containing the corrected user data or deployment configuration.
4. Update the Auto Scaling Group to use the known-good launch template version.
5. Perform a controlled instance refresh to replace affected instances.
6. Verify ALB target health, frontend responses, backend API responses, and systemd service status.

**Important:** Updating launch template settings does not automatically replace existing EC2 instances. An instance refresh or equivalent controlled replacement is required.

## 3. CloudFormation Infrastructure Rollback

If a CloudFormation stack update fails, CloudFormation can attempt to roll back to the previous stable stack configuration.

### Procedure

1. Inspect stack events and identify the failed resource.
2. Confirm whether the stack is in `UPDATE_ROLLBACK_COMPLETE`.
3. Resolve configuration or permission errors before retrying.
4. If the stack enters `UPDATE_ROLLBACK_FAILED`, investigate the cause before using `continue-update-rollback`.

Do not delete production stacks as a routine rollback method.

## 4. Database Recovery

Application rollback does not automatically reverse database schema changes.

- Use backward-compatible database migrations whenever possible.
- Take appropriate RDS snapshots before high-risk changes.
- Validate backup retention and recovery procedures before production use.
- Restore from a snapshot only after assessing data loss and application impact.

## 5. Post-Rollback Verification

After any rollback:

- Confirm ALB targets are healthy.
- Check frontend and backend application endpoints.
- Verify database connectivity.
- Review CloudWatch logs and relevant metrics.
- Record the incident, affected version, recovery actions, and follow-up fixes.

## 6. Assessment Scope

This repository provides deployment-ready infrastructure templates and documented rollback procedures. No live AWS deployment or rollback execution was required for the assessment.