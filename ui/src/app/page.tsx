"use client";

import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import { Mailer } from "./Mailer";

export default function Home() {
  return (
    <CopilotKit runtimeUrl={'/api/copilotkit'} agent="email_agent">
        <Mailer/>
    </CopilotKit>
);
}