# SmartCommute
Serverless bus delay alert system on AWS (Lambda, DynamoDB, SNS, EventBridge, API Gateway, S3)

A serverless, event-driven system on AWS that tracks bus delays on four routes (BUS-101 to BUS-104) and sends an email alert when a delay is detected. It uses simulated delay data to demonstrate the architecture.

## How it works
1. **EventBridge** triggers the FetchBus Lambda every 5 minutes.
2. **FetchBus (Lambda)** generates route data and writes all four routes to **DynamoDB**.
3. When a delay is detected, an alert goes out as an email through **SNS**.
4. A dark-themed website hosted on **S3** lets users pick a route from a dropdown.
5. The website calls **API Gateway**, which runs the **GetStatus (Lambda)** function. It reads the route from DynamoDB and returns its live status.

## AWS services used
EventBridge, Lambda (2 functions), DynamoDB, SNS, API Gateway, S3, IAM, CloudWatch

## Project structure
```
lambda/fetch_bus.py     Writes route data and triggers delay alerts
lambda/get_status.py    Returns the status of a route (route query parameter, CORS enabled)
frontend/index.html     Static website hosted on S3
```

## Security and cost controls
- Least-privilege IAM roles for each Lambda function
- AWS billing alarm and a Zero Spend Budget
- CloudWatch Logs used for monitoring and debugging

## Challenges solved
- Fixed an IAM role mismatch that caused access errors in Lambda
- Converted DynamoDB Decimal values to normal numbers so the API could return valid JSON
- Configured the EventBridge Scheduler for a 5-minute trigger

## Status
The AWS resources are turned off to avoid costs. To run it again, create the DynamoDB table and SNS topic, deploy the two Lambda functions, add the EventBridge schedule, and set the API URL in `frontend/index.html`.

## Author
Sanyukta Sasane, MCA (Cloud Computing), Pune
