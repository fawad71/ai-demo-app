"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

export function Greeter() {
  useCopilotChatSuggestions({
    instructions: "Welcome to our Hotel Service! You can:\n- View the menu\n- Add items to cart\n- View your cart\n- Place an order\n- Cancel an order"
  });

  useCoAgent({
    name: "HotelCustomerService",
  });

  return (
    <CopilotSidebar
      defaultOpen={true}
      instructions={"I am your hotel service assistant. I can help you with viewing our menu, managing your cart, and placing orders. How can I assist you today?"}
      labels={{
        title: "Hotel Service Assistant",
        initial: "Welcome! I'll show you our menu and help you place an order.",
      }}
    >
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl w-full bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">Welcome to Our Hotel Service</h1>
          
          <div className="space-y-6">
            <section className="bg-gray-50 p-6 rounded-lg">
              <h2 className="text-xl font-semibold text-gray-700 mb-4">How to Use Our Service</h2>
              <ul className="list-disc list-inside space-y-2 text-gray-600">
                <li>Browse our menu and add items to your cart</li>
                <li>Review your cart anytime</li>
                <li>Place your order when ready</li>
                <li>Track or cancel your order as needed</li>
              </ul>
            </section>

            <section className="bg-blue-50 p-6 rounded-lg">
              <h2 className="text-xl font-semibold text-blue-700 mb-4">Quick Tips</h2>
              <ul className="list-disc list-inside space-y-2 text-blue-600">
                <li>Try saying &ldquo;Show me the menu&rdquo;</li>
                <li>Add items like &ldquo;Add 2 burgers to my cart&rdquo;</li>
                <li>Check your cart with &ldquo;What&apos;s in my cart?&rdquo;</li>
                <li>Ready to order? Say &ldquo;Place my order&rdquo;</li>
              </ul>
            </section>
          </div>
        </div>
      </div>
    </CopilotSidebar>
  );
}