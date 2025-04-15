/**
 * @jest-environment jsdom
 */

const { expect } = require('@jest/globals');
require('@testing-library/jest-dom');

// Mock fetch and EmailJS before loading script
global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({ success: true }) })
);

global.emailjs = {
  send: jest.fn(() => Promise.resolve({ status: 200, text: "OK" })),
};

// Set up a mock DOM structure
document.body.innerHTML = `
  <div class="circle" data-start-date="" data-completed-date="">
    <span class="step-number">Contract</span>
    <span class="step-icon"></span>
  </div>
  <div class="circle">
    <span class="step-number">Final Measure</span>
    <span class="step-icon"></span>
  </div>
  <div class="indicator"></div>
  <div id="modal"></div>
  <form id="stepForm">
    <input id="dateStarted" />
    <input id="dateCompleted" />
    <textarea id="notes"></textarea>
  </form>
  <div id="progress-json" type="application/json">
    {"Contract":{"start_date":"03/20/25","end_date":"03/21/25","notes":"Initial"}}
  </div>
  <button class="close"></button>
`;

// Required for fetch CSRF in form submission
Object.defineProperty(document, 'cookie', {
  writable: true,
  value: 'csrftoken=testtoken',
});

// Required global for progress update
global.PROJECT_ID = "test-project-id";

// Load the JS under test
require('../JS/stepper.js');

describe("Progress stepper logic", () => {
  it("should initialize with correct progress data", () => {
    const circle = document.querySelector(".circle");
    expect(circle.dataset.startDate).toBe("03/20/25");
    expect(circle.dataset.completedDate).toBe("03/21/25");
  });

  it("should parse a valid date", () => {
    const date = global.parseDate("04/15/25");
    expect(date.getFullYear()).toBe(2025);
    expect(date.getMonth()).toBe(3); // April
    expect(date.getDate()).toBe(15);
  });

  it("should reject invalid dates", () => {
    expect(global.isValidDate("13/32/25")).toBe(false);
    expect(global.isValidDate("02/30/25")).toBe(false);
    expect(global.isValidDate("04/15/25")).toBe(true);
  });

  it("should not allow moving to next step before previous is completed", () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    const nextCircle = document.querySelectorAll(".circle")[1];
    nextCircle.click();
    expect(alertMock).toHaveBeenCalled();
    alertMock.mockRestore();
  });

  it("should trigger email and fetch on valid form submit", () => {
    document.getElementById("dateStarted").value = "04/12/25";
    document.getElementById("dateCompleted").value = "04/13/25";
    document.getElementById("notes").value = "Step note";

    document.getElementById("stepForm").dispatchEvent(new Event("submit", {
      bubbles: true,
      cancelable: true
    }));

    expect(global.fetch).toHaveBeenCalled();
    expect(global.emailjs.send).toHaveBeenCalled();
  });

  it("should reject if completion date is earlier than start date", () => {
    document.getElementById("dateStarted").value = "04/12/25";
    document.getElementById("dateCompleted").value = "04/10/25";
    document.getElementById("notes").value = "Test notes";
  
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    document.getElementById("stepForm").dispatchEvent(new Event("submit", { bubbles: true }));
  
    expect(alertMock).toHaveBeenCalledWith("Completion date cannot be earlier than the start date.");
    alertMock.mockRestore();
  });  

  it("should reject submission if all fields are empty", () => {
    document.getElementById("dateStarted").value = "";
    document.getElementById("dateCompleted").value = "";
    document.getElementById("notes").value = "";
  
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    document.getElementById("stepForm").dispatchEvent(new Event("submit", { bubbles: true }));
  
    expect(alertMock).toHaveBeenCalledWith("Please enter at least one field to update.");
    alertMock.mockRestore();
  });

  it("should log error if fetch fails", async () => {
    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: false, error: "Test failure" })
    });
  
    document.getElementById("dateStarted").value = "04/12/25";
    document.getElementById("notes").value = "Some notes";
  
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    await document.getElementById("stepForm").dispatchEvent(new Event("submit", { bubbles: true }));
  
    expect(consoleSpy).toHaveBeenCalledWith("Failed to update:", "Test failure");
    consoleSpy.mockRestore();
  });
  
  it("should catch EmailJS error", async () => {
    global.emailjs.send.mockRejectedValueOnce("Fake Email Error");
  
    document.getElementById("dateStarted").value = "04/12/25";
    document.getElementById("notes").value = "Some notes";
  
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    await document.getElementById("stepForm").dispatchEvent(new Event("submit", { bubbles: true }));
  
    expect(consoleSpy).toHaveBeenCalledWith("EmailJS error:", "Fake Email Error");
    consoleSpy.mockRestore();
  });  

  it("should auto-format MM/DD/YY in dateStarted input", () => {
    const input = document.getElementById("dateStarted");
    input.value = "";
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.value = "041225";
    input.dispatchEvent(new Event("input", { bubbles: true }));
    expect(input.value).toBe("04/12/25");
  });  

});
