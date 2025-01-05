"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import { useState } from "react";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

export function Mailer() {
  const [messageState, setMessageState] = useState<"SEND" | "CANCEL" | null>(null);
  const [pendingEmail, setPendingEmail] = useState("");
  const [resolveAction, setResolveAction] = useState<((value: string) => void) | null>(null);

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
      setPendingEmail(the_email);
      
      return new Promise<"SEND" | "CANCEL">((resolve) => {
        setResolveAction(() => (action: "SEND" | "CANCEL") => {
          setMessageState(action);
          setPendingEmail("");
          resolve(action);
        });
      });
    },
  });

  const handleConfirm = () => {
    resolveAction?.("SEND");
    setResolveAction(null);
  };

  const handleCancel = () => {
    resolveAction?.("CANCEL");
    setResolveAction(null);
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen p-4"
      data-test-id="mailer-container"
    >
      <div className="text-2xl mb-4" data-test-id="mailer-title">
        Email Q&A example
      </div>
      <div className="mb-8" data-test-id="mailer-example">
        e.g. write an email to the CEO of OpenAI asking for a meeting
      </div>

      <div className="w-full max-w-2xl">
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

        {pendingEmail && (
          <div className="bg-blue-50 rounded-lg p-6 mt-4 shadow-sm">
            <div className="font-medium text-gray-700 mb-4">Please review your email:</div>
            <div className="whitespace-pre-wrap mb-4 text-gray-600 bg-white p-4 rounded border">
              {pendingEmail}
            </div>
            <div className="flex justify-end gap-3">
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                Send
              </button>
            </div>
          </div>
        )}

        {messageState && (
          <div className="mt-4 text-center">
            {messageState === "SEND" ? (
              <div data-test-id="email-success-message" className="text-green-600">
                ✅ Sent email.
              </div>
            ) : (
              <div data-test-id="email-cancel-message" className="text-red-600">
                ❌ Cancelled sending email.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}