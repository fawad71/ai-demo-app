"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import { useState } from "react";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

export function Mailer() {

  const [messageState, setMessageState] = useState<"SEND" | "CANCEL" | null>(
    null
  );

  useCopilotChatSuggestions({
    instructions: "Write an email",
  });

  useCoAgent({
    name: "email_agent",
  });

  useCopilotAction({
    name: "EmailTool",
    available: "remote",
    parameters: [
      {
        name: "the_email",
      },
    ],

    handler: async ({ the_email }) => {
      const result = window.confirm(the_email);
      const action = result ? "SEND" : "CANCEL";
      setMessageState(action);
      return action;
    },
  });

  return (
    <div
      className="flex flex-col items-center justify-center h-screen"
      data-test-id="mailer-container"
    >
      <div className="text-2xl" data-test-id="mailer-title">
        Email Q&A example
      </div>
      <div data-test-id="mailer-example">
        e.g. write an email to the CEO of OpenAI asking for a meeting
      </div>

      <CopilotPopup
        defaultOpen={true}
        clickOutsideToClose={false}
        data-test-id="mailer-popup"
        instructions="You are a helpful assistant that can help me write an email"
        labels={{
          title: "Email Assistant",
          initial: "I will help you write an email",
        }}
      />

      <div
        data-test-id="email-success-message"
        className={messageState === "SEND" ? "" : "hidden"}
      >
        ✅ Sent email.
      </div>
      <div
        data-test-id="email-cancel-message"
        className={messageState === "CANCEL" ? "" : "hidden"}
      >
        ❌ Cancelled sending email.
      </div>
    </div>
  );
}