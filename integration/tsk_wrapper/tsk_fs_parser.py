"""
TSK File System Parser
Parses file systems using The Sleuth Kit
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.common.logger import setup_logger
from integration.tsk_wrapper.tsk_loader import TSKLoader

logger = setup_logger(__name__)

class TSKFileSystemParser:
    """Parses file systems using TSK"""
    
    def __init__(self):
        self.loader = TSKLoader()
        self.tsk = self.loader.get_tsk()
        logger.info("TSK File System Parser initialized")
    
    def open_image(self, image_path):
        """Open a forensic image or device"""
        if not self.tsk:
            logger.error("TSK not available")
            return None
        
        try:
            img_info = self.tsk.Img_Info(image_path)
            logger.info(f"Opened image: {image_path}")
            return img_info
        except Exception as e:
            logger.error(f"Failed to open image: {e}")
            return None
    
    def open_filesystem(self, image_path, offset=0):
        """Open file system from image"""
        if not self.tsk:
            return None
        
        try:
            img_info = self.open_image(image_path)
            if not img_info:
                return None
            
            fs_info = self.tsk.FS_Info(img_info, offset=offset)
            logger.info("File system opened successfully")
            return fs_info
        except Exception as e:
            logger.error(f"Failed to open filesystem: {e}")
            return None
    
    def list_files(self, image_path, path="/"):
        """List files in a directory"""
        if not self.tsk:
            return []
        
        files = []
        try:
            fs_info = self.open_filesystem(image_path)
            if not fs_info:
                return []
            
            directory = fs_info.open_dir(path=path)
            
            for entry in directory:
                if entry.info.name and entry.info.name.name:
                    name = entry.info.name.name.decode('utf-8', errors='ignore')
                    
                    if name not in ['.', '..']:
                        file_info = {
                            "name": name,
                            "size": entry.info.meta.size if entry.info.meta else 0,
                            "is_deleted": False
                        }
                        
                        if entry.info.meta and entry.info.meta.flags:
                            if entry.info.meta.flags & self.tsk.TSK_FS_META_FLAG_UNALLOC:
                                file_info["is_deleted"] = True
                        
                        files.append(file_info)
            
            logger.info(f"Found {len(files)} files")
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
    
    def find_deleted_files(self, image_path):
        """Find deleted files in image"""
        if not self.tsk:
            return []
        
        deleted_files = []
        try:
            fs_info = self.open_filesystem(image_path)
            if not fs_info:
                return []
            
            self._walk_directory(fs_info, "/", deleted_files)
            logger.info(f"Found {len(deleted_files)} deleted files")
            return deleted_files
            
        except Exception as e:
            logger.error(f"Failed to find deleted files: {e}")
            return []
    
    def _walk_directory(self, fs_info, path, deleted_files):
        """Recursively walk directories"""
        try:
            directory = fs_info.open_dir(path=path)
            
            for entry in directory:
                if entry.info.name and entry.info.name.name:
                    name = entry.info.name.name.decode('utf-8', errors='ignore')
                    
                    if name in ['.', '..']:
                        continue
                    
                    full_path = os.path.join(path, name)
                    
                    if entry.info.meta and entry.info.meta.flags:
                        if entry.info.meta.flags & self.tsk.TSK_FS_META_FLAG_UNALLOC:
                            deleted_files.append({
                                "name": name,
                                "path": full_path,
                                "size": entry.info.meta.size if entry.info.meta else 0
                            })
                    
                    if entry.info.meta and entry.info.meta.type == self.tsk.TSK_FS_META_TYPE_DIR:
                        self._walk_directory(fs_info, full_path, deleted_files)
                        
        except Exception as e:
            logger.debug(f"Walk error at {path}: {e}")

if __name__ == "__main__":
    parser = TSKFileSystemParser()
    print(f"\nTSK Parser ready: {parser.loader.is_available()}")
