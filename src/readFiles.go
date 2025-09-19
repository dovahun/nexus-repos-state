package src

import (
	"io/fs"
	"os"
	"path/filepath"
)

func ReadAllFiles(root string) (map[string][]byte, error) {
	filesContent := make(map[string][]byte)

	err := filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if !d.IsDir() { // если это файл
			data, err := os.ReadFile(path)
			if err != nil {
				return err
			}
			filesContent[path] = data
		}
		return nil
	})

	if err != nil {
		return nil, err
	}
	return filesContent, nil
}
