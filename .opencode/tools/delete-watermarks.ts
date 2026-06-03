import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Dynamically removes massive watermarks or tracking bloatware that freeze PDF files by analyzing anomalies in internal font volume.",
  args: {
    inputPath: tool.schema.string().describe("Relative or absolute path of the original PDF file infected with the watermark"),
    outputPath: tool.schema.string().describe("Destination path where the clean and optimized PDF file will be saved"),
  },
  async execute(args, context) {
    // Dynamically locate the Python script using OpenCode's current worktree
    const script = path.join(context.worktree, ".opencode/tools/delete-watermarks.py")
    
    // Secure and native execution using the Bun.$ utility provided by OpenCode
    const result = await Bun.$`python3 ${script} ${args.inputPath} ${args.outputPath}`.text()
    
    // Return the log printed to the console by Python so the model confirms operation success
    return result.trim()
  },
})