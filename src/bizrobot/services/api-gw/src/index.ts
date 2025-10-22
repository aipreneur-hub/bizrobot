import Fastify from "fastify";
import { z } from "zod";

const app = Fastify();

app.post("/intents", async (req, reply) => {
  const body = z.object({ text: z.string(), tenant_id: z.string() }).parse(req.body);
  // forward to orchestrator gRPC/HTTP (omitted)
  return { intent: "Command", entities: {}, confidence: 0.9 };
});

app.post("/execute", async (req, reply) => {
  const body = z.object({ text: z.string(), tenant_id: z.string() }).parse(req.body);
  // call orchestrator.run_workflow(...) via RPC
  return { run_id: "…" };
});

app.get("/runs/:id", async (req, reply) => {
  // return state + events + artifacts
  return { state: "SUCCEEDED", events: [] };
});

app.listen({ port: 8080 });
