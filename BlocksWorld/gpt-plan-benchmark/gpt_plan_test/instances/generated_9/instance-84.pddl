

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a f)
(ontable b)
(on c a)
(ontable d)
(on e b)
(ontable f)
(on g e)
(ontable h)
(on i g)
(clear c)
(clear d)
(clear h)
(clear i)
)
(:goal
(and
(on a d)
(on b f)
(on c b)
(on e g)
(on f a)
(on g c)
(on h i))
)
)


