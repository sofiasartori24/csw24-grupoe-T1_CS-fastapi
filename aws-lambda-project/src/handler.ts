export const handler = async (event: any): Promise<any> => {
    // Process the incoming event
    console.log("Received event:", JSON.stringify(event, null, 2));

    // Your processing logic here

    // Return a response
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: "Hello from AWS Lambda!",
            input: event,
        }),
    };
};