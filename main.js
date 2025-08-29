// 이 파일은 포트폴리오 페이지의 동적인 기능을 추가하기 위해 사용됩니다.
// GitHub API를 사용해 최신 커밋 정보를 가져오거나
// 페이지 내 인터랙티브한 요소를 추가할 수 있습니다.

document.addEventListener('DOMContentLoaded', () => {
    console.log('포트폴리오 페이지가 성공적으로 로드되었습니다.');

    // GitHub API를 이용해 최신 커밋 정보를 가져오는 함수 (예시)
    // 실제 사용 시 'your-github-id'와 'your-repo'를 본인 정보로 변경해야 합니다.
    async function fetchLatestCommit() {
        const url = 'https://api.github.com/repos/your-github-id/your-repo/commits';
        try {
            const response = await fetch(url);
            const data = await response.json();
            if (data && data.length > 0) {
                const latestCommit = data[0];
                const commitMessage = latestCommit.commit.message;
                const commitDate = new Date(latestCommit.commit.author.date).toLocaleDateString('ko-KR');
                
                console.log(`최신 커밋: ${commitMessage} (${commitDate})`);
                // 페이지에 정보를 표시하는 로직을 여기에 추가할 수 있습니다.
            }
        } catch (error) {
            console.error('GitHub API 호출 중 오류 발생:', error);
        }
    }

    // fetchLatestCommit();

    // 페이지 스크롤 이벤트에 따라 특정 효과를 주는 로직 (예시)
    // 섹션이 화면에 보일 때 애니메이션 효과를 줄 수 있습니다.
    const sections = document.querySelectorAll('section');
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });

    // 버튼 클릭 시 메시지를 표시하는 기능 (예시)
    // HTML에 <button id="myButton">버튼</button>이 있어야 작동합니다.
    const myButton = document.getElementById('myButton');
    if (myButton) {
        myButton.addEventListener('click', () => {
            alert('버튼이 클릭되었습니다!');
        });
    }
});
