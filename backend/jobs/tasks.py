import sys
import os
from celery import shared_task
from django.utils import timezone
from engine.analysis.graph_builder import build_graph
from jobs.github import clone_repo
from jobs.zip_handler import extract_zip
from jobs.cleanup import cleanup_directory
from api.models import AnalysisJob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@shared_task
def analyze_repo(job_id: str) -> None:
    """
    Core Celery task — runs the full analysis pipeline for a submitted job.

    Flow:
        PENDING → PROCESSING → COMPLETE
                             → FAILED (on any exception)

    Always cleans up the temp directory in the finally block.
    """
    tmp_dir = None

    try:
        # Fetch jon
        job = AnalysisJob.objects.get(pk=job_id)

        # Set job to processing
        job.status = 'PROCESSING'
        job.save(update_fields=['status'])

        # Get code into temp folder
        if job.source_type == 'github':
            tmp_dir = clone_repo(job.source_ref)
        else:
            from django.core.files.storage import default_storage
            file = default_storage.open(job.source_ref)
            tmp_dir = extract_zip(file)

        # Build Graph
        graph = build_graph(tmp_dir)

        # Save graph result and mark the job Complete
        job.graph_json = graph
        job.status = 'COMPLETE'
        job.completed_at = timezone.now()
        job.save(update_fields=['graph_json', 'status', 'completed_at'])

    except Exception as e:
        # Mark FAILED, store error message
        try:
            job.status = 'FAILED'
            job.error = str(e)
            job.completed_at = timezone.now()
            job.save(update_fields=['status', 'error', 'completed_at'])
        except Exception:
            pass 

    finally:
        # Clean up temp directory
        cleanup_directory(tmp_dir)