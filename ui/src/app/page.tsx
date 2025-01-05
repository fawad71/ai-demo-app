"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { Greeter } from "./greeter";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <CopilotKit runtimeUrl={'/api/copilotkit'} agent="HotelCustomerService">
        <Greeter/>
    </CopilotKit>
);
}
