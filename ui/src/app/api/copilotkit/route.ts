import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    langGraphPlatformEndpoint,
  } from '@copilotkit/runtime';
  
  import { NextRequest } from 'next/server';
   

  const serviceAdapter = new OpenAIAdapter();
  const runtime = new CopilotRuntime({
    remoteEndpoints: [
      langGraphPlatformEndpoint({
        deploymentUrl: "http://localhost:3030",
        langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
        agents: [
          {
            name: 'email_agent', 
            description: 'Email agent'
          }
        ]
      }),
    ],
  });
   
  export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: '/api/copilotkit',
    });
    return handleRequest(req);
  };