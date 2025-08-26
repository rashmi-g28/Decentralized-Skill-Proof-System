from datetime import datetime
from pathlib import Path
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas


class CertificateGenerator:
	def __init__(self, output_dir: str) -> None:
		self.output_dir = Path(output_dir)
		self.output_dir.mkdir(parents=True, exist_ok=True)

	def generate_certificate(
		self,
		user_name: str,
		skill: str,
		score: int,
		blockchain_tx_hash: Optional[str],
		issued_at: Optional[datetime] = None,
		filename_prefix: Optional[str] = None,
	) -> Path:
		issued_at = issued_at or datetime.utcnow()
		fname = f"{filename_prefix or 'certificate'}_{issued_at.strftime('%Y%m%d_%H%M%S')}.pdf"
		out_path = self.output_dir / fname

		c = canvas.Canvas(str(out_path), pagesize=A4)
		width, height = A4

		# Border
		margin = 15 * mm
		c.setStrokeColor(colors.HexColor('#444444'))
		c.setLineWidth(2)
		c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

		# Title
		c.setFont("Helvetica-Bold", 28)
		c.setFillColor(colors.HexColor('#1f2937'))
		c.drawCentredString(width / 2, height - 60 * mm, "Certificate of Skill Verification")

		# Body
		c.setFont("Helvetica", 14)
		c.setFillColor(colors.black)
		text_y = height - 85 * mm
		lines = [
			f"This certifies that {user_name}",
			f"has successfully passed the skill verification for {skill}.",
			f"Score achieved: {score}%.",
			f"Issued at: {issued_at.isoformat()} UTC",
		]
		for line in lines:
			c.drawCentredString(width / 2, text_y, line)
			text_y -= 10 * mm

		# Blockchain hash section
		c.setFont("Helvetica-Oblique", 10)
		hash_text = blockchain_tx_hash or "Pending on-chain record"
		c.drawString(margin + 5 * mm, margin + 15 * mm, f"Blockchain Tx Hash: {hash_text}")

		# Footer
		c.setFont("Helvetica", 9)
		c.setFillColor(colors.HexColor('#6b7280'))
		c.drawRightString(width - margin, margin + 10 * mm, "DSPS - Decentralized Skill Proof System")

		c.showPage()
		c.save()
		return out_path