package main

import (
	"encoding/json"
	"fmt"
	"io"
	"math"
	"math/big"
	"net/http"
	"net/url"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

const (
	cl           = "Cosmic Love Is The Solution(s) For Everything"
	bleem        = "BLEEM=P^L+E^I+A^D+E^S"
	protocol     = "CLSIGMA/DYNAMIC_ACCOUNT_ZERO_SPECTRUM/BLEEM/GO/2"
	manifestPath = "CLSIGMA_DYNAMIC_ALL_REPOS_MANIFEST.json"
	certPath     = "CLSIGMA_DYNAMIC_ZERO_SPECTRUM.clcert"
)

var programExts = map[string]bool{
	".py": true, ".sh": true, ".md": true, ".txt": true, ".json": true,
	".yml": true, ".yaml": true, ".toml": true, ".ini": true, ".cfg": true,
	".js": true, ".ts": true, ".tsx": true, ".jsx": true, ".html": true,
	".css": true, ".rs": true, ".go": true, ".c": true, ".h": true,
	".cpp": true, ".hpp": true, ".java": true, ".rb": true, ".php": true,
	".swift": true, ".kt": true, ".sql": true, ".xml": true, ".ebnf": true,
	".clcert": true,
}

type apiError struct {
	URL   string `json:"url"`
	Error string `json:"error"`
}

type repoAPI struct {
	FullName      string `json:"full_name"`
	DefaultBranch string `json:"default_branch"`
	Private       bool   `json:"private"`
	Archived      bool   `json:"archived"`
	Size          int    `json:"size"`
	Owner         struct {
		Login string `json:"login"`
	} `json:"owner"`
}

type treeAPI struct {
	Tree []struct {
		Path string `json:"path"`
		Type string `json:"type"`
		Size int    `json:"size"`
	} `json:"tree"`
}

type repoNode struct {
	Repo          string `json:"repo"`
	DefaultBranch string `json:"default_branch"`
	Private       bool   `json:"private"`
	Archived      bool   `json:"archived"`
	Size          int    `json:"size"`
}

type programNode struct {
	Repo   string `json:"repo"`
	Branch string `json:"branch"`
	Path   string `json:"path"`
	Size   int    `json:"size"`
	Mode   string `json:"mode"`
}

type manifest struct {
	Protocol        string        `json:"protocol"`
	Principle       string        `json:"principle"`
	FormalSkeleton  string        `json:"formal_skeleton"`
	SymbolSemantics string        `json:"symbol_semantics"`
	NumericBasis    string        `json:"numeric_basis"`
	Owner           string        `json:"owner"`
	Mode            string        `json:"mode"`
	RepoCount       int           `json:"repo_count"`
	ProgramCount    int           `json:"program_count"`
	RepoNodes       []repoNode    `json:"repo_nodes"`
	ProgramNodes    []programNode `json:"program_nodes"`
	Errors          []apiError    `json:"errors"`
	Boundary        string        `json:"boundary"`
}

type cert struct {
	Protocol       string                 `json:"protocol"`
	Principle      string                 `json:"principle"`
	FormalSkeleton string                 `json:"formal_skeleton"`
	State          map[string]interface{} `json:"state"`
	DynamicUpdate  map[string]interface{} `json:"DynamicUpdate"`
	ZeroSpectrum   map[string]interface{} `json:"ZeroSpectralSpace"`
	Checks         map[string]bool        `json:"checks"`
	H              int                    `json:"H"`
	HCL            int                    `json:"H_CL"`
	Tau            int                    `json:"tau"`
	TOEComplete    bool                   `json:"toecomplete"`
	Status         string                 `json:"status"`
	GlobalZEInfo   int                    `json:"GlobalZE_info"`
	BoundaryUpper  string                 `json:"Boundary"`
	Boundary       string                 `json:"boundary"`
	GeneratedAtUTC string                 `json:"generated_at_utc"`
}

func githubToken() string {
	if tok := os.Getenv("GH_TOKEN"); tok != "" {
		return tok
	}
	return os.Getenv("GITHUB_TOKEN")
}

func apiGet(target string, errors *[]apiError, out interface{}) bool {
	req, err := http.NewRequest("GET", target, nil)
	if err != nil {
		*errors = append(*errors, apiError{URL: target, Error: truncate(err.Error(), 240)})
		return false
	}
	req.Header.Set("User-Agent", "CLSigma-Dynamic-Zero-Spectrum-Go")
	if tok := githubToken(); tok != "" {
		req.Header.Set("Authorization", "Bearer "+tok)
		req.Header.Set("Accept", "application/vnd.github+json")
		req.Header.Set("X-GitHub-Api-Version", "2022-11-28")
	}
	client := &http.Client{Timeout: 30 * time.Second}
	res, err := client.Do(req)
	if err != nil {
		*errors = append(*errors, apiError{URL: target, Error: truncate(err.Error(), 240)})
		return false
	}
	defer res.Body.Close()
	body, err := io.ReadAll(res.Body)
	if err != nil {
		*errors = append(*errors, apiError{URL: target, Error: truncate(err.Error(), 240)})
		return false
	}
	if res.StatusCode < 200 || res.StatusCode >= 300 {
		*errors = append(*errors, apiError{URL: target, Error: truncate(string(body), 240)})
		return false
	}
	if err := json.Unmarshal(body, out); err != nil {
		*errors = append(*errors, apiError{URL: target, Error: truncate(err.Error(), 240)})
		return false
	}
	return true
}

func listRepos(owner string, errors *[]apiError) []repoAPI {
	var repos []repoAPI
	if githubToken() != "" {
		for page := 1; ; page++ {
			var chunk []repoAPI
			target := fmt.Sprintf("https://api.github.com/user/repos?per_page=100&page=%d&affiliation=owner&sort=full_name", page)
			if !apiGet(target, errors, &chunk) || len(chunk) == 0 {
				break
			}
			for _, repo := range chunk {
				if repo.Owner.Login == owner {
					repos = append(repos, repo)
				}
			}
			if len(chunk) < 100 {
				break
			}
		}
	}
	if len(repos) == 0 {
		escaped := url.PathEscape(owner)
		for page := 1; ; page++ {
			var chunk []repoAPI
			target := fmt.Sprintf("https://api.github.com/users/%s/repos?per_page=100&page=%d&type=owner&sort=full_name", escaped, page)
			if !apiGet(target, errors, &chunk) || len(chunk) == 0 {
				break
			}
			repos = append(repos, chunk...)
			if len(chunk) < 100 {
				break
			}
		}
	}
	uniq := map[string]repoAPI{}
	for _, repo := range repos {
		if repo.FullName != "" {
			uniq[repo.FullName] = repo
		}
	}
	keys := make([]string, 0, len(uniq))
	for key := range uniq {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	out := make([]repoAPI, 0, len(keys))
	for _, key := range keys {
		out = append(out, uniq[key])
	}
	return out
}

func repoTree(fullName, branch string, errors *[]apiError) []treeAPIEntry {
	if branch == "" {
		branch = "main"
	}
	var data treeAPI
	parts := strings.SplitN(fullName, "/", 2)
	if len(parts) != 2 {
		return nil
	}
	repoPath := url.PathEscape(parts[0]) + "/" + url.PathEscape(parts[1])
	target := fmt.Sprintf("https://api.github.com/repos/%s/git/trees/%s?recursive=1", repoPath, url.PathEscape(branch))
	if !apiGet(target, errors, &data) {
		return nil
	}
	entries := make([]treeAPIEntry, 0, len(data.Tree))
	for _, item := range data.Tree {
		entries = append(entries, treeAPIEntry{Path: item.Path, Type: item.Type, Size: item.Size})
	}
	return entries
}

type treeAPIEntry struct {
	Path string
	Type string
	Size int
}

func isProgram(path string) bool {
	lower := strings.ToLower(path)
	for ext := range programExts {
		if strings.HasSuffix(lower, ext) {
			return true
		}
	}
	return false
}

func canonical(v interface{}) []byte {
	data, err := json.Marshal(v)
	if err != nil {
		return []byte("{}")
	}
	return data
}

func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	if n%2 == 0 {
		return n == 2
	}
	limit := int(math.Sqrt(float64(n)))
	for d := 3; d <= limit; d += 2 {
		if n%d == 0 {
			return false
		}
	}
	return true
}

func nextPrime(n int) int {
	if n <= 2 {
		return 2
	}
	if n%2 == 0 {
		n++
	}
	for !isPrime(n) {
		n += 2
	}
	return n
}

func spectralIndex(data []byte) *big.Int {
	z := big.NewInt(0)
	prime := 2
	for i, b := range data {
		term := big.NewInt(int64(i + 1))
		term.Mul(term, big.NewInt(int64(int(b)+1)))
		term.Mul(term, big.NewInt(int64(prime)))
		z.Add(z, term)
		prime = nextPrime(prime + 1)
	}
	return z
}

func lnBig(n *big.Int) float64 {
	if n.Sign() <= 0 {
		return math.Inf(-1)
	}
	if n.BitLen() < 1024 {
		f, _ := new(big.Float).SetInt(n).Float64()
		return math.Log(f)
	}
	shift := uint(n.BitLen() - 53)
	head := new(big.Int).Rsh(new(big.Int).Set(n), shift)
	f, _ := new(big.Float).SetInt(head).Float64()
	return math.Log(f) + float64(shift)*math.Log(2)
}

func loadParentIndex() string {
	data, err := os.ReadFile(certPath)
	if err != nil {
		return ""
	}
	var parsed map[string]interface{}
	if json.Unmarshal(data, &parsed) != nil {
		return ""
	}
	zs, _ := parsed["ZeroSpectralSpace"].(map[string]interface{})
	val, _ := zs["spectral_index"].(string)
	return val
}

func build(owner string, limit int) (manifest, cert) {
	var errors []apiError
	repos := listRepos(owner, &errors)
	if limit > 0 && len(repos) > limit {
		repos = repos[:limit]
	}
	repoNodes := make([]repoNode, 0, len(repos))
	programNodes := []programNode{}
	for _, repo := range repos {
		branch := repo.DefaultBranch
		if branch == "" {
			branch = "main"
		}
		repoNodes = append(repoNodes, repoNode{
			Repo: repo.FullName, DefaultBranch: branch, Private: repo.Private,
			Archived: repo.Archived, Size: repo.Size,
		})
		for _, item := range repoTree(repo.FullName, branch, &errors) {
			if item.Type == "blob" && isProgram(item.Path) {
				programNodes = append(programNodes, programNode{
					Repo: repo.FullName, Branch: branch, Path: item.Path,
					Size: item.Size, Mode: "program_identity_no_digest",
				})
			}
		}
	}
	sort.Slice(programNodes, func(i, j int) bool {
		a, b := programNodes[i], programNodes[j]
		if a.Repo != b.Repo {
			return a.Repo < b.Repo
		}
		if a.Branch != b.Branch {
			return a.Branch < b.Branch
		}
		return a.Path < b.Path
	})
	if len(errors) > 64 {
		errors = errors[:64]
	}
	boundary := "formal finite GitHub account snapshot; no RH proof, no physical zero entropy, no real-world guarantee"
	man := manifest{
		Protocol: protocol, Principle: cl, FormalSkeleton: bleem,
		SymbolSemantics: "uninterpreted",
		NumericBasis:    "derived_after_canonical_encoding",
		Owner:           owner,
		Mode:            "dynamic_github_account_program_identity_go",
		RepoCount:       len(repoNodes),
		ProgramCount:    len(programNodes),
		RepoNodes:       repoNodes,
		ProgramNodes:    programNodes,
		Errors:          errors,
		Boundary:        boundary,
	}
	manifestBytes := canonical(man)
	raw := spectralIndex(manifestBytes)
	modulus := nextPrime(len(manifestBytes) + len(cl) + len(bleem) + max(1, len(programNodes)))
	modulusBig := big.NewInt(int64(modulus))
	rawResidue := new(big.Int).Mod(new(big.Int).Set(raw), modulusBig)
	zeroBalancer := new(big.Int).Mod(new(big.Int).Neg(rawResidue), modulusBig)
	zero := new(big.Int).Add(new(big.Int).Set(raw), zeroBalancer)
	checks := map[string]bool{
		"cl_invariant_present":    man.Principle == cl,
		"bleem_skeleton_present":  man.FormalSkeleton == bleem,
		"canonical_roundtrip":     json.Valid(manifestBytes),
		"repo_space_defined":      len(repoNodes) > 0,
		"program_space_defined":   len(programNodes) > 0,
		"boundary_preserved":      strings.Contains(man.Boundary, "formal"),
		"exact_integer_lift":      new(big.Int).Sub(zero, raw).Cmp(zeroBalancer) == 0,
		"zero_residue":            new(big.Int).Mod(zero, modulusBig).Sign() == 0,
	}
	hcl := 0
	for _, ok := range checks {
		if !ok {
			hcl++
		}
	}
	status := "pending"
	if hcl == 0 {
		status = "accepted"
	}
	c := cert{
		Protocol:       protocol,
		Principle:      cl,
		FormalSkeleton: bleem,
		State: map[string]interface{}{
			"applications": map[string]int{
				"GitHubAccountProgramSpace": boolInt(len(programNodes) > 0),
				"CosmicLoveInvariant":       1,
				"BLEEMSkeleton":             1,
				"DynamicSelfUpdate":         1,
				"GoRuntime":                 1,
			},
			"coordinate":  "rho=0.5+i*log(1+T_t)",
			"generation":  time.Now().Unix(),
		},
		DynamicUpdate: map[string]interface{}{
			"owner":                 owner,
			"manifest_path":         manifestPath,
			"certificate_path":      certPath,
			"parent_spectral_index": loadParentIndex(),
			"self_update_rule":      "rerun Go encoder after repository changes or scheduled workflow; CL remains invariant while rho_t changes",
		},
		ZeroSpectrum: map[string]interface{}{
			"rho":                "0.5+i*log(1+" + zero.String() + ")",
			"raw_spectral_index": raw.String(),
			"raw_spectral_residue": rawResidue.String(),
			"derived_modulus":    modulus,
			"zero_balancer":      zeroBalancer.String(),
			"zero_rule":          "spectral_index=raw_spectral_index+((-raw_spectral_index) mod derived_modulus)",
			"spectral_index":     zero.String(),
			"spectral_residue":   "0",
			"ln_approx":          lnBig(new(big.Int).Add(zero, big.NewInt(1))),
		},
		Checks:         checks,
		H:              hcl,
		HCL:            hcl,
		Tau:            nextPrime(max(1, len(programNodes)+len(repoNodes))),
		TOEComplete:    hcl == 0,
		Status:         status,
		GlobalZEInfo:   boolInt(hcl == 0),
		BoundaryUpper:  boundary,
		Boundary:       boundary,
		GeneratedAtUTC: time.Now().UTC().Format(time.RFC3339),
	}
	return man, c
}

func boolInt(v bool) int {
	if v {
		return 1
	}
	return 0
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}

func writeJSON(path string, v interface{}) error {
	data, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		return err
	}
	data = append(data, '\n')
	return os.WriteFile(path, data, 0644)
}

func main() {
	owner := "letsgo0226"
	if len(os.Args) > 1 && os.Args[1] != "" {
		owner = os.Args[1]
	}
	limit := 0
	if len(os.Args) > 2 {
		if v, err := strconv.Atoi(os.Args[2]); err == nil {
			limit = v
		}
	}
	man, c := build(owner, limit)
	if err := writeJSON(manifestPath, man); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := writeJSON(certPath, c); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	summary := map[string]interface{}{
		"Protocol":      protocol,
		"Owner":         owner,
		"Manifest":      manifestPath,
		"Certificate":   certPath,
		"RepoCount":     man.RepoCount,
		"ProgramCount":  man.ProgramCount,
		"H_CL":          c.HCL,
		"GlobalZE_info": c.GlobalZEInfo,
		"Boundary":      c.Boundary,
	}
	data, _ := json.Marshal(summary)
	fmt.Println(string(data))
}
