import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json(
    {
      detail:
        "Attempt results are stored in your browser on this Netlify deploy. Open review from the same device/session after submit.",
    },
    { status: 404 }
  );
}
