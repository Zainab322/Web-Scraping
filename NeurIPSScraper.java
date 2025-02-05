import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class NeurIPSScraper {
    private static final String USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36";
    private static final int TIMEOUT = 30000;
    private static final int THREAD_COUNT = 10;

    public static void main(String[] args) {
        String baseUrl = "https://papers.nips.cc";
        String mainPageUrl = baseUrl + "/";
        String baseDownloadPath = "D:/MyPapers/";
        List<Thread> threads = new ArrayList<>();

        try {
            Document mainDoc = fetchDocument(mainPageUrl);
            Elements yearLinks = mainDoc.select("a[href^='/paper_files/paper/']");
            List<String> years = new ArrayList<>();
            for (Element year : yearLinks) {
                years.add(baseUrl + year.attr("href"));
            }

            FileWriter textWriter = new FileWriter("NeurIPS_Papers.txt");

            for (String yearUrl : years) {
                Thread thread = new Thread(() -> {
                    try {
                        Document yearDoc = fetchDocument(yearUrl);
                        Elements paperLinks = yearDoc.select("a[href*='-Abstract-Conference.html']");
                        String year = yearUrl.replaceAll("[^0-9]", "");
                        String yearFolder = baseDownloadPath + year + "/";
                        new File(yearFolder).mkdirs();
                        List<Thread> paperThreads = new ArrayList<>();
                        
                        for (Element paper : paperLinks) {
                            Thread paperThread = new Thread(() -> scrapePaper(paper, baseUrl, textWriter, yearFolder));
                            paperThread.start();
                            paperThreads.add(paperThread);

                            if (paperThreads.size() >= THREAD_COUNT) {
                                for (Thread t : paperThreads) {
                                    try {
                                        t.join();
                                    } catch (InterruptedException e) {
                                        System.err.println("Thread interrupted: " + e.getMessage());
                                    }
                                }
                                paperThreads.clear();
                            }
                        }
                    } catch (IOException e) {
                        System.err.println("Error fetching year URL: " + yearUrl);
                    }
                });
                thread.start();
                threads.add(thread);
            }

            for (Thread thread : threads) {
                thread.join();
            }
            
            textWriter.close();
            System.out.println("\nData saved to NeurIPS_Papers.txt");
        } catch (IOException | InterruptedException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    private static void scrapePaper(Element paper, String baseUrl, FileWriter textWriter, String downloadFolder) {
        try {
            String paperUrl = baseUrl + paper.attr("href");
            Document paperDoc = fetchDocument(paperUrl);

            Element titleElement = paperDoc.selectFirst("meta[name='citation_title']");
            String title = titleElement != null ? titleElement.attr("content").trim() : "No title";

            Elements authorElements = paperDoc.select("meta[name='citation_author']");
            List<String> authorsList = new ArrayList<>();
            for (Element author : authorElements) {
                authorsList.add(author.attr("content"));
            }
            String authors = authorsList.isEmpty() ? "Unknown Authors" : String.join(", ", authorsList);

            Element abstractElement = paperDoc.selectFirst("p");
            String abstractText = abstractElement != null ? abstractElement.text().trim() : "No abstract available";

            Element pdfMeta = paperDoc.selectFirst("meta[name='citation_pdf_url']");
            String pdfUrl = pdfMeta != null ? pdfMeta.attr("content") : "No PDF available";

            String paperData = "Title: " + title + "\n" +
                    "Authors: " + authors + "\n" +
                    "Abstract: " + abstractText + "\n" +
                    "URL: " + paperUrl + "\n" +
                    "PDF: " + pdfUrl + "\n" +
                    "--------------------------------------------------\n";

            synchronized (textWriter) {
                textWriter.write(paperData);
                textWriter.flush();
            }

            if (!pdfUrl.equals("No PDF available")) {
                String pdfFileName = downloadFolder + File.separator + title.replaceAll("[\\/:*?\"<>|]", "_") + ".pdf";
                downloadPDF(pdfUrl, pdfFileName);
            }
        } catch (IOException e) {
            System.err.println("Error scraping paper: " + paper.attr("href"));
        }
    }

    private static Document fetchDocument(String url) throws IOException {
        return Jsoup.connect(url)
                .userAgent(USER_AGENT)
                .timeout(TIMEOUT)
                .get();
    }

    private static void downloadPDF(String fileUrl, String savePath) {
        try {
            URL url = new URL(fileUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setRequestProperty("User-Agent", USER_AGENT);
            connection.setConnectTimeout(TIMEOUT);
            connection.setReadTimeout(TIMEOUT);

            try (InputStream in = connection.getInputStream()) {
                Files.copy(in, Paths.get(savePath));
                System.out.println("PDF Downloaded: " + savePath);
            }
        } catch (IOException e) {
            System.err.println("Failed to download: " + fileUrl);
        }
    }
}
