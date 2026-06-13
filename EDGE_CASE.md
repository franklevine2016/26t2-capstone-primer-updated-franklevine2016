# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation

1. Edge Case Description
When there is no student data stored in the database and a request is sent to the /stats endpoint. This scenario is not specified in the project requirements, so it is regarded as an undefined edge case.

2. Solution
1. Set the total number of students (count) to 0.
2. Set the average score, minimum score and maximum score to 0.
3. Return a standard 200 status code without errors or 404 responses.
