"""
Version control service for report management
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from backend.models.report_models import ReportVersion
from backend.config import get_settings
import shutil


class VersionControlService:
    """
    Service for managing report versions and revisions
    """

    def __init__(self):
        self.settings = get_settings()
        self.archive_dir = Path(self.settings.reports_output_dir) / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Version metadata file
        self.metadata_file = self.archive_dir / "versions.json"
        self._load_metadata()

    def _load_metadata(self):
        """Load version metadata from file"""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def _save_metadata(self):
        """Save version metadata to file"""
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2, default=str)

    def create_version(
        self,
        report_id: str,
        file_path: str,
        changes: List[str],
        created_by: str = "system",
    ) -> ReportVersion:
        """
        Create a new version of a report

        Args:
            report_id: Report identifier
            file_path: Path to report file
            changes: List of changes in this version
            created_by: User who created this version

        Returns:
            ReportVersion object
        """
        # Get current version number
        versions = self.get_versions(report_id)
        if versions:
            last_version = versions[-1].version
            major, minor = map(int, last_version.split("."))
            new_version = f"{major}.{minor + 1}"
        else:
            new_version = "1.0"

        # Create archive copy
        source_path = Path(file_path)
        archive_path = self.archive_dir / f"{report_id}_v{new_version}{source_path.suffix}"

        shutil.copy2(source_path, archive_path)

        # Create version object
        version = ReportVersion(
            report_id=report_id,
            version=new_version,
            created_at=datetime.now(),
            changes=changes,
            file_path=str(archive_path),
            created_by=created_by,
        )

        # Save metadata
        if report_id not in self.metadata:
            self.metadata[report_id] = []

        self.metadata[report_id].append({
            "version": version.version,
            "created_at": version.created_at.isoformat(),
            "changes": version.changes,
            "file_path": version.file_path,
            "created_by": version.created_by,
        })

        self._save_metadata()

        return version

    def get_versions(self, report_id: str) -> List[ReportVersion]:
        """
        Get all versions of a report

        Args:
            report_id: Report identifier

        Returns:
            List of ReportVersion objects
        """
        if report_id not in self.metadata:
            return []

        versions = []
        for version_data in self.metadata[report_id]:
            versions.append(
                ReportVersion(
                    report_id=report_id,
                    version=version_data["version"],
                    created_at=datetime.fromisoformat(version_data["created_at"]),
                    changes=version_data["changes"],
                    file_path=version_data["file_path"],
                    created_by=version_data["created_by"],
                )
            )

        return versions

    def get_version(self, report_id: str, version: str) -> Optional[ReportVersion]:
        """
        Get specific version of a report

        Args:
            report_id: Report identifier
            version: Version number

        Returns:
            ReportVersion object or None
        """
        versions = self.get_versions(report_id)
        for v in versions:
            if v.version == version:
                return v

        return None

    def get_latest_version(self, report_id: str) -> Optional[ReportVersion]:
        """
        Get latest version of a report

        Args:
            report_id: Report identifier

        Returns:
            Latest ReportVersion object or None
        """
        versions = self.get_versions(report_id)
        return versions[-1] if versions else None

    def compare_versions(
        self, report_id: str, version1: str, version2: str
    ) -> Dict[str, Any]:
        """
        Compare two versions of a report

        Args:
            report_id: Report identifier
            version1: First version number
            version2: Second version number

        Returns:
            Comparison results
        """
        v1 = self.get_version(report_id, version1)
        v2 = self.get_version(report_id, version2)

        if not v1 or not v2:
            return {"error": "One or both versions not found"}

        return {
            "version1": {
                "version": v1.version,
                "created_at": v1.created_at.isoformat(),
                "changes": v1.changes,
            },
            "version2": {
                "version": v2.version,
                "created_at": v2.created_at.isoformat(),
                "changes": v2.changes,
            },
            "time_difference": (v2.created_at - v1.created_at).total_seconds(),
        }

    def delete_version(self, report_id: str, version: str) -> bool:
        """
        Delete a specific version

        Args:
            report_id: Report identifier
            version: Version number

        Returns:
            True if deleted, False otherwise
        """
        version_obj = self.get_version(report_id, version)

        if not version_obj:
            return False

        # Delete file
        file_path = Path(version_obj.file_path)
        if file_path.exists():
            file_path.unlink()

        # Remove from metadata
        self.metadata[report_id] = [
            v for v in self.metadata[report_id] if v["version"] != version
        ]

        self._save_metadata()

        return True

    def list_all_reports(self) -> List[str]:
        """
        List all reports with versions

        Returns:
            List of report IDs
        """
        return list(self.metadata.keys())

    def get_report_summary(self, report_id: str) -> Dict[str, Any]:
        """
        Get summary of a report's versions

        Args:
            report_id: Report identifier

        Returns:
            Summary dictionary
        """
        versions = self.get_versions(report_id)

        if not versions:
            return {"report_id": report_id, "version_count": 0}

        return {
            "report_id": report_id,
            "version_count": len(versions),
            "first_version": versions[0].version,
            "latest_version": versions[-1].version,
            "created_at": versions[0].created_at.isoformat(),
            "last_updated": versions[-1].created_at.isoformat(),
            "total_changes": sum(len(v.changes) for v in versions),
        }
