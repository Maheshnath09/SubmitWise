import zipfile
import os
import json
from typing import Dict, Any
from io import BytesIO


class ZIPBundler:
    """Create ZIP bundles with all project files"""
    
    def _ensure_dict(self, data: Any, default: Any = None) -> Dict:
        """Ensure data is a dictionary, parsing JSON if needed"""
        if data is None:
            return default if default is not None else {}
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                return parsed if isinstance(parsed, dict) else (default if default is not None else {})
            except json.JSONDecodeError:
                return default if default is not None else {}
        if isinstance(data, dict):
            return data
        return default if default is not None else {}
    
    def create_bundle(
        self,
        project_data: Dict[str, Any],
        docx_bytes: bytes,
        pptx_bytes: bytes
    ) -> bytes:
        """
        Create ZIP bundle with all project deliverables
        
        Args:
            project_data: Project JSON
            docx_bytes: DOCX report bytes
            pptx_bytes: PPTX slides bytes
            
        Returns:
            ZIP file as bytes
        """
        # Ensure project_data is a dict
        project_data = self._ensure_dict(project_data)
        
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add metadata.json
            project_metadata = self._ensure_dict(project_data.get('metadata', {}))
            metadata = {
                'title': project_data.get('title', 'Project'),
                'difficulty': project_data.get('difficulty', 'N/A'),
                'timeline_days': project_data.get('timeline_days', 0),
                'generated_at': project_metadata.get('generated_at', ''),
                'keywords': project_data.get('keywords', [])
            }
            zip_file.writestr('metadata.json', json.dumps(metadata, indent=2))
            
            # Add README.md
            readme_content = self._generate_readme(project_data)
            zip_file.writestr('README.md', readme_content)
            
            # Add report.docx
            zip_file.writestr('report.docx', docx_bytes)
            
            # Add slides.pptx
            zip_file.writestr('slides.pptx', pptx_bytes)
            
            # Add code files
            code_snippets = project_data.get('code_snippets', [])
            if code_snippets:
                for snippet in code_snippets:
                    filename = snippet.get('filename', 'code.txt')
                    content = snippet.get('content', '')
                    
                    # Remove markdown code fences if present
                    if content.startswith('```'):
                        lines = content.split('\n')
                        content = '\n'.join(lines[1:-1]) if len(lines) > 2 else content
                    
                    zip_file.writestr(f'code/{filename}', content)
            
            # Add file structure info
            impl = self._ensure_dict(project_data.get('implementation', {}))
            if impl.get('file_structure'):
                structure_content = json.dumps(impl['file_structure'], indent=2)
                zip_file.writestr('file_structure.json', structure_content)
            
            # Add viva questions
            viva_questions = project_data.get('viva_questions', [])
            if viva_questions:
                viva_content = "# Viva Questions\n\n"
                for idx, q in enumerate(viva_questions, 1):
                    viva_content += f"## Question {idx}\n"
                    # Handle both string questions and dict questions
                    if isinstance(q, str):
                        viva_content += f"**Q:** {q}\n\n"
                    elif isinstance(q, dict):
                        viva_content += f"**Q:** {q.get('q', q.get('question', ''))}\n\n"
                        if q.get('expected_answer') or q.get('answer'):
                            viva_content += f"**Expected Answer:** {q.get('expected_answer', q.get('answer', ''))}\n\n"
                        if q.get('difficulty'):
                            viva_content += f"**Difficulty:** {q.get('difficulty', 'N/A')}\n\n"
                        if q.get('hint'):
                            viva_content += f"**Hint:** {q.get('hint', '')}\n\n"
                    viva_content += "---\n\n"
                
                zip_file.writestr('viva_questions.md', viva_content)
            
            # Add rubric
            rubric = project_data.get('rubric', [])
            if rubric:
                rubric_content = "# Marking Rubric\n\n"
                rubric_content += "| Criteria | Weight |\n"
                rubric_content += "|----------|--------|\n"
                for item in rubric:
                    # Handle both string rubric and dict rubric
                    if isinstance(item, str):
                        rubric_content += f"| {item} | N/A |\n"
                    elif isinstance(item, dict):
                        rubric_content += f"| {item.get('criteria', '')} | {item.get('weight', 0)}% |\n"
                
                zip_file.writestr('rubric.md', rubric_content)
        
        zip_buffer.seek(0)
        return zip_buffer.read()
    
    def _generate_readme(self, project_data: Dict[str, Any]) -> str:
        """Generate README.md content"""
        readme = f"""# {project_data.get('title', 'Project')}

## Abstract
{project_data.get('abstract', '')}

## Difficulty Level
{project_data.get('difficulty', 'N/A')}

## Timeline
{project_data.get('timeline_days', 0)} days

## Keywords
{', '.join(project_data.get('keywords', []))}

## Modules
"""
        
        for idx, module in enumerate(project_data.get('modules', []), 1):
            # Handle both string modules and dict modules
            if isinstance(module, str):
                readme += f"\n### {idx}. {module}\n"
            elif isinstance(module, dict):
                readme += f"\n### {idx}. {module.get('name', 'Module')}\n"
                readme += f"{module.get('description', '')}\n"
                if module.get('weeks'):
                    readme += f"**Duration:** {module.get('weeks', 0)} weeks\n"
        
        readme += "\n## Implementation\n"
        impl = self._ensure_dict(project_data.get('implementation', {}))
        readme += f"- **Language:** {impl.get('language', 'N/A')}\n"
        readme += f"- **Frameworks:** {', '.join(impl.get('frameworks', []))}\n"
        
        readme += "\n## Requirements\n"
        readme += "\n### Hardware\n"
        for hw in project_data.get('hardware_required', []):
            readme += f"- {hw}\n"
        
        readme += "\n### Software\n"
        for sw in project_data.get('software_required', []):
            readme += f"- {sw}\n"
        
        readme += "\n## Files Included\n"
        readme += "- `report.docx` - Complete project report\n"
        readme += "- `slides.pptx` - Presentation slides\n"
        readme += "- `code/` - Source code files\n"
        readme += "- `viva_questions.md` - Viva preparation questions\n"
        readme += "- `rubric.md` - Marking criteria\n"
        readme += "- `metadata.json` - Project metadata\n"
        
        readme += "\n---\n"
        readme += "Generated by ProjectGen - AI-Powered College Project Generator\n"
        
        return readme


# Singleton instance
zip_bundler = ZIPBundler()
