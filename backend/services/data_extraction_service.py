"""
Data extraction service for various file formats
"""
import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
from pathlib import Path
import csv


class DataExtractionService:
    """
    Service for extracting test data from various file formats
    """

    async def extract_from_excel(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from Excel files

        Args:
            file_path: Path to Excel file

        Returns:
            Extracted data dictionary
        """
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            data = {}

            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                # Convert to dictionary, handling NaN values
                data[sheet_name] = df.fillna("").to_dict(orient="records")

            return {
                "success": True,
                "sheets": data,
                "sheet_names": excel_file.sheet_names,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "sheets": {}}

    async def extract_from_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from CSV files

        Args:
            file_path: Path to CSV file

        Returns:
            Extracted data dictionary
        """
        try:
            df = pd.read_csv(file_path)
            return {
                "success": True,
                "data": df.fillna("").to_dict(orient="records"),
                "columns": df.columns.tolist(),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "data": []}

    async def extract_from_json(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from JSON files

        Args:
            file_path: Path to JSON file

        Returns:
            Extracted data dictionary
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            return {"success": True, "data": data}

        except Exception as e:
            return {"success": False, "error": str(e), "data": {}}

    async def extract_from_xml(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from XML files

        Args:
            file_path: Path to XML file

        Returns:
            Extracted data dictionary
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Convert XML to dictionary
            data = self._xml_to_dict(root)

            return {"success": True, "data": data}

        except Exception as e:
            return {"success": False, "error": str(e), "data": {}}

    async def extract_from_ivc(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from I-V curve files (.ivc format)
        Common format for solar simulator output

        Args:
            file_path: Path to IVC file

        Returns:
            Extracted I-V curve data
        """
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            # Parse header for metadata
            metadata = {}
            data_start_index = 0

            for i, line in enumerate(lines):
                if line.strip().startswith("#") or line.strip().startswith("//"):
                    # Parse metadata from comments
                    if ":" in line:
                        key, value = line.strip("# /").split(":", 1)
                        metadata[key.strip()] = value.strip()
                elif line.strip() and not line.startswith("Voltage") and not line.startswith("V"):
                    data_start_index = i
                    break

            # Extract I-V curve data
            # Assuming format: Voltage(V), Current(A), Power(W)
            iv_data = []
            for line in lines[data_start_index:]:
                if line.strip() and not line.startswith("V"):
                    parts = line.strip().split(",") if "," in line else line.strip().split()
                    if len(parts) >= 2:
                        try:
                            voltage = float(parts[0])
                            current = float(parts[1])
                            power = float(parts[2]) if len(parts) > 2 else voltage * current
                            iv_data.append({
                                "voltage": voltage,
                                "current": current,
                                "power": power,
                            })
                        except ValueError:
                            continue

            # Calculate key parameters
            if iv_data:
                max_power_point = max(iv_data, key=lambda x: x["power"])
                voc = max(iv_data, key=lambda x: x["voltage"])["voltage"]
                isc = max(iv_data, key=lambda x: x["current"])["current"]

                metadata.update({
                    "Voc": voc,
                    "Isc": isc,
                    "Vmp": max_power_point["voltage"],
                    "Imp": max_power_point["current"],
                    "Pmax": max_power_point["power"],
                    "FF": (max_power_point["power"] / (voc * isc)) if (voc * isc) > 0 else 0,
                })

            return {
                "success": True,
                "metadata": metadata,
                "iv_curve": iv_data,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "metadata": {}, "iv_curve": []}

    async def parse_test_result_file(self, file_path: str) -> Dict[str, Any]:
        """
        Automatically detect file type and extract data

        Args:
            file_path: Path to file

        Returns:
            Extracted data
        """
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension in [".xlsx", ".xls"]:
            return await self.extract_from_excel(file_path)
        elif extension == ".csv":
            return await self.extract_from_csv(file_path)
        elif extension == ".json":
            return await self.extract_from_json(file_path)
        elif extension == ".xml":
            return await self.extract_from_xml(file_path)
        elif extension in [".ivc", ".txt"]:
            return await self.extract_from_ivc(file_path)
        else:
            return {
                "success": False,
                "error": f"Unsupported file format: {extension}",
            }

    def _xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        Convert XML element to dictionary

        Args:
            element: XML element

        Returns:
            Dictionary representation
        """
        result = {}

        # Add attributes
        if element.attrib:
            result["@attributes"] = element.attrib

        # Add text content
        if element.text and element.text.strip():
            if len(element) == 0:  # No children
                return element.text.strip()
            else:
                result["#text"] = element.text.strip()

        # Add children
        for child in element:
            child_data = self._xml_to_dict(child)

            if child.tag in result:
                # Multiple children with same tag - convert to list
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data

        return result if result else None

    async def extract_images_info(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Extract information about images (for inclusion in reports)

        Args:
            image_paths: List of image file paths

        Returns:
            List of image information dictionaries
        """
        images_info = []

        for image_path in image_paths:
            try:
                from PIL import Image

                with Image.open(image_path) as img:
                    images_info.append({
                        "path": image_path,
                        "format": img.format,
                        "size": img.size,
                        "mode": img.mode,
                        "exists": True,
                    })

            except Exception as e:
                images_info.append({
                    "path": image_path,
                    "error": str(e),
                    "exists": False,
                })

        return images_info

    async def calculate_statistics(self, data: List[float]) -> Dict[str, float]:
        """
        Calculate statistical parameters for test data

        Args:
            data: List of numerical values

        Returns:
            Statistical parameters
        """
        if not data:
            return {}

        try:
            import numpy as np

            arr = np.array(data)
            return {
                "mean": float(np.mean(arr)),
                "median": float(np.median(arr)),
                "std_dev": float(np.std(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "range": float(np.max(arr) - np.min(arr)),
                "count": len(data),
            }

        except Exception as e:
            return {"error": str(e)}
