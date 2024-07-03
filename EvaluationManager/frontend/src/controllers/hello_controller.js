import { Controller } from "@stimulus/core"

export default class extends Controller {
    static targets = ["output"]

    connect() {
        this.outputTarget.textContent = "Hello, Stimulus!"
    }
}
